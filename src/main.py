#!/usr/bin/env python3


"""
TODO: This is wrong, change it:

IEEE Papers Data Extraction Script
==================================
This script fetches research papers from the IEEE Xplore API based on a specific search query.
The query and optional file name are provided as command-line arguments.
"""

import time
from config.scheduler import Scheduler


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
