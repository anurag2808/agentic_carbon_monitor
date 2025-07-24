import threading
import agent
import tracker
print("\n🚀 Starting Agent + Tracker via main.py\n")


if __name__ == "__main__":
    print("\n=== 🚀 Launching Agent + Job Simulator ===")

    t1 = threading.Thread(target=tracker.job_simulator, daemon=True)
    t2 = threading.Thread(target=agent.run_autonomous_agent, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
