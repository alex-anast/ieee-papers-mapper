#!/usr/bin/env python3

"""
TODO: This is wrong, change it:

IEEE Papers Data Extraction Script
==================================
This script fetches research papers from the IEEE Xplore API based on a specific search query.
The query and optional file name are provided as command-line arguments.
"""

import os
import logging
import pandas as pd
import config.config as cfg
from database import Database
from get_papers import get_papers
from process_papers import process_papers
from classify_papers import classify_all_papers

logger = logging.getLogger("ieee_logger")

def run_pipeline():
    """
    Executes the full data pipeline:
    1. Fetch new papers.
    2. Preprocess and classify them.
    3. Store final results in the database.

    Returns:
        bool: True if new papers were processed, False otherwise.
    """
    db = Database(
        name="ieee_papers",
        filepath=os.path.join(cfg.ROOT_DIR, cfg.DATA_DIR),
    )
    logger.debug("Initializing database...")
    db.initialize()  # Handles cases where db doesn't exist or not all tables

    # Step 1: Get new papers
    logger.debug("Retrieving papers from IEEE database...")
    df_raw = get_papers(
        query="machine learning",
        start_year=2020,
        max_records=50,
    )
    if df_raw.empty:
        logger.info("No new papers fetched.")
        logger.debug("Returning False if no papers fetched.")
        return False

    # Step 2: Process data
    logger.debug("Processing papers...")
    df_processed = process_papers(df_raw)

    # Step 3: Insert new data into the database
    logger.debug("Storing data in SQLite database...")
    for _, row in df_processed.iterrows():
        try:
            db.insert_full_paper(row)
        except Exception as e:
            logger.error(
                f"Error inserting paper with is_number {row['is_number']}: {e}"
            )

    logger.debug("Classifying papers...")
    df_unclassified = pd.read_sql_query(
        sql="""
            SELECT p.paper_id, pr.prompt_text
            FROM papers p
            JOIN prompts pr ON p.paper_id = pr.paper_id
            WHERE NOT EXISTS (
                SELECT 1 FROM classification c WHERE c.paper_id = p.paper_id
            )
        """,
        con=db.connection,
    )
    if df_unclassified.empty:
        logger.debug("No unclassified papers found")
    else:
        logger.debug("Starting timer")
        df_classified = classify_all_papers(df_unclassified, timer=True)
        del df_unclassified
        df_classified.to_sql("classification", db.connection, if_exists="append", index=False)
        logger.info(f"Classified and stored {len(df_classified)} papers.")

    db.close()
    return True