#!/usr/bin/env python3

"""
TODO: This is wrong, change it:

IEEE Papers Data Extraction Script
==================================
This script fetches research papers from the IEEE Xplore API based on a specific search query.
The query and optional file name are provided as command-line arguments.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from data.pipeline import run_pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ieee_logger")


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        """
        Start the scheduler and schedule the data pipeline task.
        """
        logger.info("Starting scheduler...")
        self.scheduler.add_job(
            run_pipeline,  # ...
            trigger=IntervalTrigger(hours=6),
            id="pipeline_job",
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info("Scheduler started.")

    def stop(self):
        """
        Stop the scheduler gracefully.
        """
        logger.info("Stopping scheduler...")
        self.scheduler.shutdown()
        logger.info("Scheduler stopped.")
