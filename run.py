import time
from app.generate_dataset import run
from app.config import settings

WAIT_SECONDS = getattr(settings, "WAIT_SECONDS", 60) 

def main_loop():
    print(f"🔁 Starting data generation loop every {WAIT_SECONDS} seconds. Press Ctrl+C to stop.\n")
    
    try:
        while True:
            run()
            print(f"✅ Run complete. Waiting {WAIT_SECONDS} seconds...\n")
            time.sleep(WAIT_SECONDS)
    except KeyboardInterrupt:
        print("🛑 Stopped by user.")

if __name__ == "__main__":
    main_loop()
