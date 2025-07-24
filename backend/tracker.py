import time
import random
from shared import JOB_QUEUE

def job_simulator():
    teams = ["ml-team", "data-eng", "research"]
    print("\n--- 🧪 Job Simulator RUNNING ---")
    while True:
        time.sleep(random.uniform(3, 8))
        team_to_log = random.choice(teams)
        random_emission = round(random.uniform(50, 400), 2)
        job = {"team": team_to_log, "task_emission": random_emission}
        JOB_QUEUE.append(job)
        print(f"[SIMULATOR]: New job → {job}")

if __name__ == "__main__":
    job_simulator()
