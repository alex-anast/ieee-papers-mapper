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
from data_extraction import fetch_papers_and_store_csv
from data_preprocessing import preprocess_csv
import classification
import database
import webapp
import config


def main():
    # Step 1: Extract Data
    # - Use the `data_extraction` module to fetch raw papers from the IEEE API.
    print("Step 1: Fetching data...")
    # fetch_papers_and_store_csv(query="machine learning")

    # - Ensure API limits are respected using a scheduler.

    # Step 2: Preprocess Raw Data
    # - Convert raw CSVs into a structured format for classification.
    # - Assume that preprocessed and raw files have the same name.
    print("Step 2: Preprocessing data...")

    # if not os.path.exists(args.file):
    #     raise FileNotFoundError(f"File '{args.file}' does not exist.")

    # Store paths of directories
    fn_path_raw = os.path.join(config.ROOT_DIR, config.DATA_RAW_DIR)
    fn_path_preprocessed = os.path.join(config.ROOT_DIR, config.DATA_PROCESSED_DIR)

    # Get list of files in each directory
    ls_raw = os.listdir(fn_path_raw)
    ls_preprocessed = os.listdir(fn_path_preprocessed)

    print(ls_raw, type(ls_raw))  # List of files in raw directory
    print(
        ls_preprocessed, type(ls_preprocessed)
    )  # List of files in preprocessed directory

    # If a file exists in raw but not in preprocessed, preprocess it
    for filename in ls_raw:
        if filename not in ls_preprocessed:
            preprocess_csv(
                file_path=os.path.join(fn_path_raw, filename),
                output_dir=fn_path_preprocessed,
            )

    # - Schedule preprocessing for new arrivals.

    # Step 3: Classify Papers
    # - Use a pre-trained zero-shot transformer to classify papers.
    print("Step 3: Classifying papers...")
    print("Step 3: Not implemented yet.")
    # classify_all_files(input_dir="./data/processed/", output_dir="./data/classified/")

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
