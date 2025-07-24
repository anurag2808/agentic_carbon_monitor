# from carbon_api import get_carbon_intensity

# zones = ["US-CAL-CISO", "EU-DE", "IN-DL", "SG"]
# results = []

# for zone in zones:
#     result = get_carbon_intensity(zone)
#     results.append(result)

# # Sort by lowest carbon intensity
# sorted_results = sorted([r for r in results if r["intensity"] is not None], key=lambda x: x["intensity"])

# print("Carbon intensity by region:")
# for r in sorted_results:
#     print(f"{r['zone']}: {r['intensity']} {r['unit']}")
import time
from shared import JOB_QUEUE, LIVE_DATABASE
from carbon_api import get_carbon_intensity

def run_autonomous_agent():
    print("\n--- 🤖 Carbon-Aware Agent RUNNING ---")

    while True:
        try:
            job = JOB_QUEUE.popleft()
            team = job["team"]
            task_emission = job["task_emission"]
            print(f"[AGENT]: Processing job: {job}")

            # Step 1: Check team usage
            usage = LIVE_DATABASE[team]["current_usage_gco2"]
            new_usage = usage + task_emission
            budget = LIVE_DATABASE[team]["budget_gco2"]
            remaining = budget - new_usage

            # Step 2: Query carbon intensity
            zones = ["US-CAL-CISO"]  # You can reintroduce more mock/real later
            results = []
            for zone in zones:
                result = get_carbon_intensity(zone)
                if result["intensity"]:
                    results.append(result)
            sorted_results = sorted(results, key=lambda x: x["intensity"])
            greenest = sorted_results[0] if sorted_results else {"zone": "unknown", "intensity": 0}

            # Step 3: Decision log
            print(f"[AGENT]: Best Zone: {greenest['zone']} ({greenest['intensity']} gCO₂/kWh)")

            # Step 4: Update usage
            LIVE_DATABASE[team]["current_usage_gco2"] = new_usage
            if remaining < 0:
                print(f"[AGENT]: 🚨 Team '{team}' exceeded budget! Remaining: {remaining:.2f}")
            else:
                print(f"[AGENT]: ✅ Team '{team}' OK. Remaining: {remaining:.2f}")

        except IndexError:
            time.sleep(2)

if __name__ == "__main__":
    run_autonomous_agent()
