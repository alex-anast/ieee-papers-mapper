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

from data_extraction import fetch_papers_and_store_csv
import data_preprocessing
import classification
import database
import webapp


def main():
    # Step 1: Extract Data
    # - Use the `data_extraction` module to fetch raw papers from the IEEE API.
    # - Ensure API limits are respected using a scheduler.
    print("Step 1: Fetching data...")
    fetch_papers_and_store_csv(query="machine learning")

    # Step 2: Preprocess Raw Data
    # - Convert raw CSVs into a structured format for classification.
    # - Schedule preprocessing for new arrivals.
    print("Step 2: Preprocessing data...")
    print("Step 2: Not implemented yet.")
    # preprocess_all_csv(input_dir="./data/raw/", output_dir="./data/processed/")

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
