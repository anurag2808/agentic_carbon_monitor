import time
import random
import json
import threading
from collections import deque

# --- Environment Simulation ---

# 1. The Live Database (The Agent's memory or state)
_LIVE_DATABASE = {
    "ml-team": {"budget_gco2": 2000, "current_usage_gco2": 0},
    "data-eng": {"budget_gco2": 3500, "current_usage_gco2": 0},
    "research": {"budget_gco2": 1500, "current_usage_gco2": 0},
}

# 2. The Job Queue (The source of tasks for the Agent)
_JOB_QUEUE = deque()

# 3. The Job Simulator (Simulates other services creating tasks)
def job_simulator():
    """
    Runs in the background to simulate other systems adding jobs to the queue.
    """
    teams = ["ml-team", "data-eng", "research"]
    while True:
        time.sleep(random.uniform(3, 8))
        team_to_log = random.choice(teams)
        random_emission = round(random.uniform(50, 400), 2)
        job = {"team": team_to_log, "task_emission": random_emission}
        _JOB_QUEUE.append(job)
        print(f"\n[SIMULATOR]: New job submitted to queue -> {job}")

# --- The Autonomous Agent ---

def get_team_budget_data(team_name: str) -> dict | None:
    """Fetches data from the live database."""
    return _LIVE_DATABASE.get(team_name)

def update_team_usage(team_name: str, new_usage: float):
    """Writes updated usage back to the live database."""
    if team_name in _LIVE_DATABASE:
        _LIVE_DATABASE[team_name]["current_usage_gco2"] = new_usage

def run_autonomous_agent():
    """
    The main loop for the agent. It runs forever, checking for and processing jobs.
    """
    print("--- 🤖 Autonomous Carbon Budget Agent is now RUNNING ---")
    print("--- Monitoring job queue for new tasks... ---")

    while True:
        try:
            job = _JOB_QUEUE.popleft()
            print(f"[AGENT]: Found job. Processing: {job}")
            
            team = job["team"]
            task_emission = job["task_emission"]

            budget_info = get_team_budget_data(team)
            if budget_info:
                current_usage = budget_info["current_usage_gco2"]
                new_total_usage = current_usage + task_emission
                remaining_budget = budget_info["budget_gco2"] - new_total_usage
                
                update_team_usage(team, new_total_usage)
                
                # --- MODIFIED SECTION: Check status and print OK or WARNING ---
                if remaining_budget < 0:
                    print(f"[AGENT]: 🚨 WARNING! Team '{team}' has exceeded their budget.")
                    print(f"         Remaining Budget: {remaining_budget:.2f} gCO₂")
                else:
                    print(f"[AGENT]: ✅ OK! Team '{team}' is within budget.")
                    print(f"         Remaining Budget: {remaining_budget:.2f} gCO₂")
                # --- END OF MODIFIED SECTION ---
            
        except IndexError:
            # Queue is empty, wait and check again.
            time.sleep(2)

if __name__ == "__main__":
    simulator_thread = threading.Thread(target=job_simulator, daemon=True)
    simulator_thread.start()
    
    run_autonomous_agent()