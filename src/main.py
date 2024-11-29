from config.scheduler import Scheduler
import time


def main():
    scheduler = Scheduler()

    try:
        scheduler.start()
        print("Scheduler is running. Press Ctrl+C to stop.")

        while True:
            time.sleep(1)  # Keeps the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()
        print("Scheduler stopped gracefully.")


if __name__ == "__main__":
    main()
