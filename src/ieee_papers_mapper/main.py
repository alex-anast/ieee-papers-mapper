#!/usr/bin/env python3


"""
IEEE Papers Scheduler Script
============================

This script starts the scheduler for fetching, processing, and classifying research
papers from the IEEE Xplore API at specified intervals.

Usage:
    python3 <script_name>.py [--weeks WEEKS] [--days DAYS]
                             [--hours HOURS] [--minutes MINUTES]
                             [--seconds SECONDS]

Arguments:
    --weeks     : Interval in weeks (default: 0).
    --days      : Interval in days (default: 0).
    --hours     : Interval in hours (default: 0).
    --minutes   : Interval in minutes (default: 0).
    --seconds   : Interval in seconds (default: 0).

The scheduler runs the pipeline in the background at the specified interval.
Press Ctrl+C to stop the scheduler gracefully.
"""


import time
import logging
import argparse
from ieee_papers_mapper.data.pipeline import run_pipeline
from ieee_papers_mapper.config.scheduler import Scheduler
from ieee_papers_mapper.config.logging_config import setup_logging

logger = setup_logging()


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
        job=run_pipeline,
        weeks=args.weeks,
        days=args.days,
        hours=args.hours,
        minutes=args.minutes,
        seconds=args.seconds,
    )

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
