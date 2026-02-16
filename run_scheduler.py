import time
import schedule
from main import main

def job():
    print("--- [Scheduled Job Start] ---")
    try:
        main()
    except Exception as e:
        print(f"Job Failed: {e}")
    print("--- [Scheduled Job End] ---\n")

schedule.every(10).seconds.do(job)

if __name__ == "__main__":
    print("Scheduler Started... (Press Ctrl+C to stop)")
    
    while True:
        schedule.run_pending()
        time.sleep(1)