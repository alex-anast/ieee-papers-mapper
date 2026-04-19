#!/usr/bin/env python3

"""
IEEE Papers Pipeline
====================
Orchestrates the full data pipeline: fetching papers from the IEEE Xplore API,
processing them into structured records, storing them in DuckDB, and classifying
unclassified papers using a transformer-based zero-shot classifier.

Progress is tracked incrementally via a JSON file so that interrupted runs can
resume from where they left off.
"""

import os
import json
import time
import uuid
import logging
from ieee_papers_mapper.config import config as cfg
from ieee_papers_mapper.config.metrics import (
    pipeline_runs,
    pipeline_duration,
    papers_fetched,
    api_requests,
    api_latency,
    total_papers_gauge,
    unclassified_gauge,
    last_successful_run,
)
from ieee_papers_mapper.exceptions import IEEEApiError
from ieee_papers_mapper.data.database import Database
from ieee_papers_mapper.data.repository import PaperRepository
from ieee_papers_mapper.data.get_papers import get_papers
from ieee_papers_mapper.data.process_papers import process_papers
from ieee_papers_mapper.data.classify_papers import classify_all_papers

logger = logging.getLogger("ieee_logger")


class ProgressTracker:
    def __init__(self, filename: str, config_dir: str):
        self.filepath = os.path.join(config_dir, filename)

    def load(self) -> dict[str, int]:
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath) as f:
            return json.load(f)

    def save(self, progress: dict[str, int]) -> None:
        with open(self.filepath, "w") as f:
            json.dump(progress, f, indent=4)


def run_pipeline() -> bool:
    """
    Executes the full data pipeline.

    Fetches new papers incrementally per category, stores them via the
    repository, then classifies any unclassified papers.

    Returns
    -------
    bool
        True if new papers were fetched and stored, False otherwise.
    """
    run_id = str(uuid.uuid4())[:8]
    logger.info("Pipeline run started", extra={"run_id": run_id})
    start = time.monotonic()

    db = Database(name="ieee_papers", filepath=cfg.SRC_DIR)
    db.initialise()
    repo = PaperRepository(db.connection)
    tracker = ProgressTracker(cfg.JSON_FILENAME, cfg.CONFIG_DIR)

    try:
        new_papers = _fetch_and_store(repo, tracker, run_id)
        if new_papers:
            _classify_new_papers(repo, run_id)
        pipeline_runs.labels(status="success").inc()
        total_papers_gauge.set(repo.count_papers())
        unclassified_gauge.set(repo.count_unclassified())
        last_successful_run.set_to_current_time()
        return new_papers
    except Exception:
        pipeline_runs.labels(status="failure").inc()
        raise
    finally:
        pipeline_duration.observe(time.monotonic() - start)
        db.close()


def _fetch_and_store(repo: PaperRepository, tracker: ProgressTracker, run_id: str) -> bool:
    """
    Fetches papers from the IEEE API for each configured category and stores
    them via the repository.

    Parameters
    ----------
    repo : PaperRepository
        Repository used to persist paper records.
    tracker : ProgressTracker
        Tracks per-category pagination progress across runs.
    run_id : str
        Identifier for the current pipeline run, used in log context.

    Returns
    -------
    bool
        True if at least one new paper was retrieved, False otherwise.
    """
    progress = tracker.load()
    new_papers = False

    for category in cfg.CATEGORIES:
        start_record = progress.get(category, 1)
        try:
            while True:
                logger.debug(
                    f"Fetching IEEE data for category '{category}', start_record={start_record}...",
                    extra={"run_id": run_id},
                )
                api_start = time.monotonic()
                df_raw = get_papers(
                    query=category,
                    api_key=cfg.IEEE_API_KEY,
                    start_year=cfg.IEEE_API_START_YEAR,
                    start_record=start_record,
                    max_records=cfg.IEEE_API_MAX_RECORDS,
                )
                api_latency.labels(category=category).observe(time.monotonic() - api_start)
                api_requests.labels(category=category, status="success").inc()

                if df_raw.empty:
                    logger.info(
                        f"No new papers found for category: '{category}'",
                        extra={"run_id": run_id},
                    )
                    break

                new_papers = True
                papers = process_papers(df_raw)
                papers_fetched.labels(category=category).inc(len(papers))

                for paper in papers:
                    repo.insert_full_paper(paper)

                start_record += cfg.IEEE_API_MAX_RECORDS
                progress[category] = start_record
                tracker.save(progress)

                if len(df_raw) < cfg.IEEE_API_MAX_RECORDS:
                    logger.info(
                        f"Completed retrieval for category '{category}'.",
                        extra={"run_id": run_id},
                    )
                    break
        except IEEEApiError as e:
            api_requests.labels(category=category, status="error").inc()
            logger.error(
                f"API error for category '{category}': {e}",
                extra={"run_id": run_id},
            )
            continue

    return new_papers


def _classify_new_papers(repo: PaperRepository, run_id: str) -> None:
    """
    Retrieves unclassified papers and stores their classifications.

    Parameters
    ----------
    repo : PaperRepository
        Repository used to query and persist classification records.
    run_id : str
        Identifier for the current pipeline run, used in log context.
    """
    df_unclassified = repo.get_unclassified_papers()
    if df_unclassified.empty:
        return
    classifications = classify_all_papers(df_unclassified)
    repo.insert_classifications(classifications)
    logger.info(
        f"Classified and stored {len(classifications)} papers.",
        extra={"run_id": run_id},
    )


def load_progress(filename: str) -> dict:
    """
    Load the progress tracking JSON file.

    Parameters
    ----------
    filename : str
        The name of the JSON file storing progress data.

    Returns
    -------
    dict
        A dictionary where each category maps to its last fetched start_record.
    """
    tracker = ProgressTracker(filename, cfg.CONFIG_DIR)
    return tracker.load()


def save_progress(filename: str, progress: dict) -> None:
    """
    Save progress tracking data to a JSON file.

    Parameters
    ----------
    filename : str
        The name of the JSON file to save progress.
    progress : dict
        A dictionary mapping each category to its current start_record.
    """
    tracker = ProgressTracker(filename, cfg.CONFIG_DIR)
    tracker.save(progress)
