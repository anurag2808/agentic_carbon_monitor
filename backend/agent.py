# backend/agent.py
import time
import json
import os # <-- Import os
from shared import JOB_QUEUE, LIVE_DATABASE
from carbon_api import get_carbon_intensity

# --- NEW: Define path for the shared JSON file in the project root ---
# This makes the path independent of where you run the script from
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
JSON_FILE_PATH = os.path.join(PROJECT_ROOT, "carbon_data.json")
# --------------------------------------------------------------------

ZONES_TO_MONITOR = ["US-CAL-CISO", "EU-DE", "IN-DL", "SG", "FR", "GB"]

def update_carbon_intensity_data():
    """Fetches carbon data, sorts it, and writes it to a shared JSON file."""
    print("[AGENT]: Fetching latest carbon intensity data...")
    results = [get_carbon_intensity(zone) for zone in ZONES_TO_MONITOR]
    
    valid_results = [r for r in results if r.get("intensity") is not None]
    sorted_results = sorted(valid_results, key=lambda x: x["intensity"])
    
    # --- MODIFIED PART ---
    # Write to the centrally located JSON file
    try:
        with open(JSON_FILE_PATH, "w") as f:
            json.dump(sorted_results, f)
    except IOError as e:
        print(f"[AGENT]: ERROR - Could not write to {JSON_FILE_PATH}: {e}")
    # --- END MODIFICATION ---
    
    if sorted_results:
        greenest = sorted_results[0]
        print(f"[AGENT]: Carbon data updated. Greenest zone is {greenest['zone']} at {greenest['intensity']} gCO₂eq/kWh.")
    else:
        print("[AGENT]: Warning - could not fetch any valid carbon data.")

# The rest of your agent.py file (run_autonomous_agent, etc.) remains unchanged.
def run_autonomous_agent():
    print("\n--- 🤖 Carbon-Aware Agent RUNNING ---")
    update_carbon_intensity_data()
    last_update_time = time.time()
    update_interval = 60
    while True:
        if time.time() - last_update_time > update_interval:
            update_carbon_intensity_data()
            last_update_time = time.time()
        try:
            job = JOB_QUEUE.popleft()
            region = job["region"]
            team = job["team"]
            task_emission = job["task_emission"]
            print(f"[AGENT]: Processing job for team '{team}' in region '{region}'")
            try:
                team_data = LIVE_DATABASE[region][team]
                new_usage = team_data["current_usage_gco2"] + task_emission
                remaining = team_data["budget_gco2"] - new_usage
                team_data["current_usage_gco2"] = new_usage
                if remaining < 0:
                    print(f"  └── 🚨 WARNING! Exceeded budget. Remaining: {remaining:.2f} gCO₂")
                else:
                    print(f"  └── ✅ OK! Within budget. Remaining: {remaining:.2f} gCO₂")
            except KeyError:
                print(f"  └── 🛑 ERROR! No budget found for team '{team}' in region '{region}'.")
        except IndexError:
            time.sleep(2)

if __name__ == "__main__":
    run_autonomous_agent()

    