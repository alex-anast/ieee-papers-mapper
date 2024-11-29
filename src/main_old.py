#!/usr/bin/env python3

"""
Main pipeline to automate the IEEE paper workflow.
Steps:
1. Fetch papers from the IEEE API (data extraction).
2. Preprocess raw data to make it suitable for classification.
3. Classify papers into predefined categories using an encoder-only transformer.
4. Store classified results in an SQLite database.
5. (Optional) Visualize and serve data via a web app.
"""

import os
import pandas as pd
import logging
import config
from get_papers import get_papers
from process_papers import process_papers
from classify_papers import classify_all_papers
from database import Database

logger = logging.getLogger(__name__)


def main():
    # Initialize database
    db = Database(
        name="ieee_papers",
        filepath=os.path.join(config.ROOT_DIR, config.DATA_DIR),
    )
    db.initialize()

    logger.info("Step 1: Fetching data...")
    # df_raw = pd.DataFrame()
    # df_raw = get_papers(  # TODO: Remove hardcoded constants
    #     query="machine learning",
    #     start_year=2000,
    #     max_records=10,
    # )

    # For debugging
    df_raw = pd.read_csv(
        "/home/alex-anast/workspace/ieee-papers-mapper/data/raw/machine_learning_20241126_160712.csv"
    )

    logger.info("Step 2: Processing data...")
    df_processed = process_papers(df_raw)

    logger.info("Step 3: Storing data in SQLite database")
    for _, row in df_processed.iterrows():
        try:
            db.insert_full_paper(row)
        except Exception as e:
            logger.error(
                f"Error inserting paper with is_number {row['is_number']}: {e}"
            )

    logger.info("Step 4: Classifying papers...")
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
        logger.info("No unclassified papers found")
    else:
        df_classified = classify_all_papers(df_unclassified)
        del df_unclassified
        df_classified.to_sql(
            "classification", db.connection, if_exists="append", index=False
        )
        logger.info(f"Classified and stored {len(df_classified)} papers.")

    logger.info("Step 5: Launching web app...")

    # db.close()


if __name__ == "__main__":
    main()
