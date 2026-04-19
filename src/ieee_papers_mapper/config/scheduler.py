#!/usr/bin/env python3

"""
IEEE Papers Scheduler
=====================
Wraps APScheduler to execute a configurable job callable at specified intervals.
The job (typically the data pipeline) runs in a background thread, allowing the
main process to remain responsive.
"""

import logging
from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger("ieee_logger")

_DEFAULT_INTERVAL = {"weeks": 1}


class Scheduler:
    """
    Schedules a callable to run periodically using APScheduler.
    """

    def __init__(self, job: Callable, **interval_kwargs):
        """
        Parameters
        ----------
        job : Callable
            The callable to execute on each trigger.
        interval_kwargs : dict
            Time interval keyword arguments accepted by APScheduler's
            IntervalTrigger (weeks, days, hours, minutes, seconds).
            If all values are zero or none are provided, defaults to weekly.
        """
        self.job = job
        self.scheduler = BackgroundScheduler(timezone="UTC")
        non_zero = {k: v for k, v in interval_kwargs.items() if v}
        if non_zero:
            self.interval_kwargs = non_zero
        else:
            logger.debug("No non-zero interval provided, defaulting to 1 week")
            self.interval_kwargs = _DEFAULT_INTERVAL

    def start(self) -> None:
        """
        Starts the scheduler. Runs the job immediately, then repeats at
        the configured interval.
        """
        logger.info(
            f"Starting scheduler with trigger interval: {self.interval_kwargs}..."
        )
        self.scheduler.add_job(
            self.job,
            trigger=IntervalTrigger(**self.interval_kwargs),
            id="pipeline_job",
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info("Scheduler started, running job immediately...")
        self.job()

    def stop(self) -> None:
        """
        Stops the scheduler gracefully.
        """
        logger.info("Stopping scheduler...")
        self.scheduler.shutdown()
        logger.info("Scheduler stopped.")
