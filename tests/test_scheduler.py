#!/usr/bin/env python3

import time
import pytest
from unittest.mock import MagicMock
from ieee_papers_mapper.config.scheduler import Scheduler, _DEFAULT_INTERVAL


def test_immediate_execution_on_start():
    job = MagicMock()
    scheduler = Scheduler(job=job, seconds=60)
    scheduler.start()
    try:
        job.assert_called_once()
    finally:
        scheduler.stop()


def test_all_zero_intervals_default_to_weekly():
    job = MagicMock()
    scheduler = Scheduler(job=job, weeks=0, days=0, hours=0, minutes=0, seconds=0)
    assert scheduler.interval_kwargs == _DEFAULT_INTERVAL


def test_no_intervals_default_to_weekly():
    job = MagicMock()
    scheduler = Scheduler(job=job)
    assert scheduler.interval_kwargs == _DEFAULT_INTERVAL


def test_non_zero_intervals_preserved():
    job = MagicMock()
    scheduler = Scheduler(job=job, hours=6, minutes=0)
    assert scheduler.interval_kwargs == {"hours": 6}


def test_stop_is_clean():
    job = MagicMock()
    scheduler = Scheduler(job=job, seconds=60)
    scheduler.start()
    scheduler.stop()
    job.assert_called_once()
