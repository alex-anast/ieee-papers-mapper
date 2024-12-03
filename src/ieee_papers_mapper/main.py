#!/usr/bin/env python3


"""
TODO: This is wrong, change it:

IEEE Papers Data Extraction Script
==================================
This script fetches research papers from the IEEE Xplore API based on a specific search query.
The query and optional file name are provided as command-line arguments.
"""

import time
import sys
import logging
import argparse
from data.pipeline import run_pipeline
from config.scheduler import Scheduler

# Setup logger
logger = logging.getLogger("ieee_logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    # Set up argument parsing for setting the scheduler trigger intervals
    parser = argparse.ArgumentParser(description="Start the IEEE papers scheduler.")
    parser.add_argument("--weeks", type=int, default=0, help="Interval in weeks.")
    parser.add_argument("--days", type=int, default=0, help="Interval in days.")
    parser.add_argument("--hours", type=int, default=0, help="Interval in hours.")
    parser.add_argument("--minutes", type=int, default=0, help="Interval in minutes.")
    parser.add_argument("--seconds", type=int, default=0, help="Interval in seconds.")
    args = parser.parse_args()

    scheduler = Scheduler(
        weeks=args.weeks,
        days=args.days,
        hours=args.hours,
        minutes=args.minutes,
        seconds=args.seconds,
    )

    try:
        # scheduler.start()
        print("Scheduler is running. Press Ctrl+C to stop.")
        run_pipeline()
        while True:
            time.sleep(1)  # Keeps the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()
        print("Scheduler stopped gracefully.")


if __name__ == "__main__":
    main()
