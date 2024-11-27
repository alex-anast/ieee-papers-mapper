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
from data_preprocessing import preprocess_csv
from classification import classify_papers
from database import Database
import webapp
import config


def main():
    # Initialize database
    # db = Database(name="ieee_papers", filepath=os.path.join(ROOT_DIR, DATA_DIR))
    # if not db.exists:
    #     db.initialize()

    print("Step 1: Fetching data...")
    df_raw = pd.DataFrame()
    df_raw = get_papers(  # TODO: Remove hardcoded constants
        query="machine learning",
        start_year=2000,
        max_records=10,
    )

    print("Step 2: Preprocessing data...")
    preprocess_papers(
        file_path=os.path.join(fn_path_raw, filename),
        output_dir=fn_path_preprocessed,
    )


    # - Schedule preprocessing for new arrivals.

    # Step 3: Classify Papers
    # - Use a pre-trained zero-shot transformer to classify papers.
    print("Step 3: Classifying papers...")

    fn_path_classified = os.path.join(config.ROOT_DIR, config.DATA_CLASSIFIED_DIR)
    ls_classified = os.listdir(fn_path_classified)

    # If a file exists in processed but not in classified, classify it
    for filename in ls_preprocessed:
        if filename not in ls_classified:
            classify_papers(
                file_path=os.path.join(fn_path_raw, filename),
                output_dir=fn_path_preprocessed,
            )

    # Step 4: Store Classified Data in SQLite
    # - Insert the classified data into an SQLite database for querying and visualization.
    print("Step 4: Storing data in SQLite database...")
    print("Step 4: Not implemented yet.")
    # store_in_database(data_dir="./data/classified/")

    # Step 5: Serve and Visualize Data (Optional)
    # - Launch a web app to provide insights into the database.
    print("Step 5: Launching web app...")
    print("Step 5: Not implemented yet.")
    # launch_webapp()


if __name__ == "__main__":
    main()
