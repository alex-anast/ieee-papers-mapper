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
from get_papers import get_papers
from process_papers import process_papers
from classification import classify_papers
from database import Database
import webapp
import config


def main():
    # Initialize database
    db = Database(
        name="ieee_papers",
        filepath=os.path.join(config.ROOT_DIR, config.DATA_DIR),
    )
    if not db.exists:
        db.initialize()

    print("Step 1: Fetching data...")
    # df_raw = pd.DataFrame()
    # df_raw = get_papers(  # TODO: Remove hardcoded constants
    #     query="machine learning",
    #     start_year=2000,
    #     max_records=10,
    # )

    # For debugging
    df_raw = pd.read_csv("/home/alex-anast/workspace/ieee-papers-mapper/data/raw/machine_learning_20241126_160712.csv")

    print("Step 2: Processing data...")
    df_processed = process_papers(df_raw)

    print("Step 3: Storing data in SQLite database")

    # - Schedule preprocessing for new arrivals.

    print("Step 3: Classifying papers...")
    print("Step 4: Storing data in SQLite database...")
    print("Step 5: Launching web app...")


if __name__ == "__main__":
    main()
