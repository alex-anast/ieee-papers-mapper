#!/usr/bin/env python3

"""
IEEE Papers Data Extraction Script
==================================
This script fetches research papers from the IEEE Xplore API based on a specific search query.
The query and optional file name are provided as command-line arguments.
"""

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from typing import Any, List, Optional
import argparse
import config


def fetch_papers(query: str, start_year: str = "2020", max_records: int = 10) -> List:
    """
    Fetches research papers from the IEEE API.

    Parameters:
        query (str): The search query for the API.
        start_year (str): The starting year for the search.
        max_records (int): Maximum number of records to fetch (max 200).

    Returns:
        list: A list of articles retrieved from the API.
    """
    params = {
        "apikey": config.IEEE_API_KEY,
        "format": "json",
        "content_type": "Journals",
        "start_year": start_year,
        "max_records": max_records,
        "sort_field": "article_number",
        "sort_order": "asc",
        "querytext": query,
        "start_record": 1,
    }

    try:
        response = requests.get(config.BASE_URL, params=params)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error during requests to {config.BASE_URL}: {req_err}")
    except KeyError:
        print("No articles found in the response.")
    return []


def save_to_csv(data: List, filename: str, data_dir_path: Optional[str] = None) -> None:
    """
    Saves the extracted data to a CSV file.

    Parameters:
        data (list): The list of articles to save.
        filename (str): The name of the output CSV file.
        data_dir_path (str, optional): Directory path to save the file. Defaults to DATA_RAW_DIR.
    """
    if data_dir_path is None:
        data_dir_path = config.DATA_RAW_DIR

    file_path = os.path.join(data_dir_path, filename)

    if not data:
        print(f"No data to save for query. Filename: {filename}")
        return

    df = pd.json_normalize(data)
    os.makedirs(data_dir_path, exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")


def fetch_papers_and_store_csv(query: str, csv_filename: Optional[str] = None) -> None:
    if not csv_filename:
        csv_filename = query.replace(" ", "_").lower()

    papers = fetch_papers(query=query)
    if papers:
        save_to_csv(data=papers, filename=csv_filename)
    else:
        print(f"TERMINATE: No data fetched for query:\n    {query}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract research papers from IEEE Xplore API."
    )
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        type=str,
        help="The search query for the data extraction (e.g., 'energy', 'machine learning').",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Optional: The name of the CSV file to save the results. Defaults to the query name.",
    )
    args = parser.parse_args()

    csv_filename = args.file if args.file else None
    fetch_papers_and_store_csv(args.query, csv_filename)
