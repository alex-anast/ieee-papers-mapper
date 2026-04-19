#!/usr/bin/env python3

"""
IEEE Papers Scheduler
=====================
Wraps APScheduler to execute a configurable job callable at specified intervals.
The job (typically the data pipeline) runs in a background thread, allowing the
main process to remain responsive.
"""

import logging
import datetime
from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from zoneinfo import ZoneInfoNotFoundError as ZINFError

logger = logging.getLogger("ieee_logger")


class Scheduler:
    """
    Schedules a callable to run periodically using APScheduler.
    """

    def __init__(self, job: Callable, **interval_kwargs):
        """
        Initializes the Scheduler with a job and a time interval.

        Parameters
        ----------
        job : Callable
            The callable to execute on each trigger.
        interval_kwargs : dict
            Time interval keyword arguments accepted by APScheduler's
            IntervalTrigger (weeks, days, hours, minutes, seconds).
        """
        datetime.UTC  # Ensures UTC is recognised
        self.job = job
        self.scheduler = BackgroundScheduler({"apscheduler.timezone": "UTC"})
        if not interval_kwargs:
            logger.debug("No time interval provided for scheduler, default: 1 week")
            self.interval_kwargs = {"weeks": 1}
        else:
            self.interval_kwargs = interval_kwargs

    def start(self) -> None:
        """
        Starts the scheduler and registers the job.

        Raises
        ------
        ZINFError
            If the host timezone configuration is incompatible.
        """
        logger.info(
            f"Starting scheduler with trigger interval: {self.interval_kwargs}..."
        )
        try:
            self.scheduler.add_job(
                self.job,
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

    def stop(self) -> None:
        """
        Stops the scheduler gracefully.
        """
        logger.info("Stopping scheduler...")
        self.scheduler.shutdown()
        logger.info("Scheduler stopped.")
