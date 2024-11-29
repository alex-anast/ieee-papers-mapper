#!/usr/bin/env python3

"""
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from data.pipeline import run_pipeline
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        """
        Start the scheduler and schedule the data pipeline task.
        """
        logger.info("Starting scheduler...")
        self.scheduler.add_job(
            run_pipeline,
            trigger=IntervalTrigger(hours=6),  # Runs every 6 hours
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
