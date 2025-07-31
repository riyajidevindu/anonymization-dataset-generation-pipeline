import time
import argparse
import threading
from app import generate_dataset, extract_pii_values
from app.config import settings

WAIT_SECONDS = getattr(settings, "WAIT_SECONDS", 60) 

def main():
    parser = argparse.ArgumentParser(description="Dataset Generation Pipeline")
    parser.add_argument(
        "action",
        choices=["generate", "extract_pii"],
        nargs='?',
        default="generate",
        help="Action to perform"
    )
    args = parser.parse_args()

    if args.action == "generate":
        main_loop()
    elif args.action == "extract_pii":
        run_pii_extraction()

def run_pii_extraction():
    stop_event = threading.Event()
    
    # Run the PII extraction in a separate thread so the main thread can catch the interrupt
    pii_thread = threading.Thread(target=extract_pii_values.run, args=(stop_event,))
    pii_thread.start()
    
    try:
        # Wait for the thread to complete, but allow KeyboardInterrupt to be caught
        while pii_thread.is_alive():
            pii_thread.join(timeout=1)
    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C detected. Sending stop signal to threads...")
        stop_event.set()
        # Wait for the thread to finish cleaning up
        pii_thread.join()
        print("🛑 All threads stopped. Exiting.")

def main_loop():
    print(f"🔁 Starting data generation loop every {WAIT_SECONDS} seconds. Press Ctrl+C to stop.\n")
    
    try:
        while True:
            generate_dataset.run()
            print(f"✅ Run complete. Waiting {WAIT_SECONDS} seconds...\n")
            time.sleep(WAIT_SECONDS)
    except KeyboardInterrupt:
        print("🛑 Stopped by user.")

if __name__ == "__main__":
    main()
