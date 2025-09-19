# tracker.py
import time
import random
from shared import JOB_QUEUE, LIVE_DATABASE

def job_simulator():
    """
    Simulates other systems adding region-specific jobs to the queue.
    """
    print("\n--- 🧪 Job Simulator RUNNING ---")

    # Create a list of all valid (region, team) combinations to draw from.
    valid_jobs_pool = []
    for region, teams in LIVE_DATABASE.items():
        for team in teams.keys():
            valid_jobs_pool.append({"region": region, "team": team})

    while True:
        time.sleep(random.uniform(4, 10))

        # Create a random job for a valid region and team
        job_details = random.choice(valid_jobs_pool)
        random_emission = round(random.uniform(50, 400), 2)

        job = {
            "region": job_details["region"],
            "team": job_details["team"],
            "task_emission": random_emission
        }

        JOB_QUEUE.append(job)
        print(f"\n[SIMULATOR]: New job submitted → {job}")

if __name__ == "__main__":
    job_simulator()

    