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

logger = logging.getLogger("ieee_logger")


class Scheduler:
    def __init__(self, **interval_kwargs):
        self.scheduler = BackgroundScheduler()
        if interval_kwargs is None:
            logger.debug("No time interval provided for scheduler, default: 1 week")
            # TODO: make self.interval_kwargs to be 1 week for IntervalTrigger
        else:
            self.interval_kwargs = interval_kwargs

    def start(self):
        """
        Start the scheduler and schedule the data pipeline task.
        """
        logger.info(f"Starting scheduler with trigger interval: {self.interval_kwargs} ...")
        self.scheduler.add_job(
            run_pipeline,  # ...
            trigger=IntervalTrigger(**self.interval_kwargs),
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
