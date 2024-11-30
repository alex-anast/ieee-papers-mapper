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
from config.scheduler import Scheduler

# Setup logger
logger = logging.getLogger("ieee_logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


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
