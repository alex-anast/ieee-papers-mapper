#!/usr/bin/env python3

"""
IEEE Papers Scheduler
=====================
This script automates the process of retrieving, processing, and classifying research papers from the IEEE Xplore API.
It uses APScheduler to periodically trigger the data pipeline task at specified intervals.

Features:
- Automatic retrieval of new papers based on predefined categories.
- Incremental processing and classification of papers.
- Configurable scheduling intervals.

Dependencies:
- APScheduler for scheduling.
- Logging for structured logging.
- ZoneInfo for handling time zone errors.
"""

import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from zoneinfo import ZoneInfoNotFoundError as ZINFError
from data.pipeline import run_pipeline

logger = logging.getLogger("ieee_logger")


class Scheduler:
    """
    A class for scheduling the IEEE papers data pipeline using APScheduler.
    """

    def __init__(self, **interval_kwargs):
        """
        Initializes the Scheduler instance with a specified time interval.

        Parameters:
        ----------
        interval_kwargs : dict
            A dictionary containing the time intervals for the scheduler 
            (weeks, days, hours, minutes, seconds).

        Raises:
        -------
        ValueError:
            If invalid interval values are provided.
        """
        datetime.UTC  # Ensures UTC is recognized
        self.scheduler = BackgroundScheduler({"apscheduler.timezone": "UTC"})
        if not interval_kwargs:
            logger.debug("No time interval provided for scheduler, default: 1 week")
            self.interval_kwargs = {"weeks": 1}  # Default interval
        else:
            self.interval_kwargs = interval_kwargs

    def start(self):
        """
        Starts the scheduler and schedules the data pipeline task.

        The scheduler runs the `run_pipeline` function at intervals specified 
        during initialization.

        Raises:
        -------
        ZINFError:
            If the system's time zone configuration is incorrect.
        """
        logger.info(
            f"Starting scheduler with trigger interval: {self.interval_kwargs}..."
        )
        try:
            self.scheduler.add_job(
                run_pipeline,
                trigger=IntervalTrigger(**self.interval_kwargs),
                id="pipeline_job",
                replace_existing=True,
            )
        except ZINFError as zinfe:
            logger.error(
                "Host timezone is not in alignment with the predicted one. Sync your environment."
            )
            logger.error(zinfe)
            raise ZINFError
        self.scheduler.start()
        logger.info("Scheduler started.")

    def stop(self):
        """
        Stops the scheduler gracefully.

        Ensures that all jobs are terminated and resources are cleaned up.
        """
        logger.info("Stopping scheduler...")
        self.scheduler.shutdown()
        logger.info("Scheduler stopped.")
