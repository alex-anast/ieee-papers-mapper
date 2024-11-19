#!/usr/bin/env python3

"""
IEEE Papers Data Extraction Script
==================================
This script fetches research papers from the IEEE Xplore API based on specific search queries.
It saves the extracted data in a CSV format for further analysis.

Make sure to set your IEEE API key in a `.env` file as follows:
    IEEE_API_KEY=your_api_key_here
"""

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from typing import Any, List

# Environment variables
load_dotenv()
IEEE_API_KEY = os.getenv("IEEE_API_KEY")

# Constants
BASE_URL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
DATA_DIR = "./data/raw/"
# TODO: Make the quering more intelligent, with placeholders etc. SQL in the background
QUERIES = [
    "onboard charger OR on-board charger OR integrated charger",
    "dc-dc converter OR dc/dc converter",
    "inverter OR dc/ac converter OR dc-ac converter",
    "gallium nitride",
    "silicon carbide",
]
# For finally naming the file
CATEGORY_MAP = {
    QUERIES[0]: "obc",
    QUERIES[1]: "dcdc",
    QUERIES[2]: "inverter",
    QUERIES[3]: "gan",
    QUERIES[4]: "sic",
}


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
        "apikey": IEEE_API_KEY,
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
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error during requests to {BASE_URL}: {req_err}")
    except KeyError:
        print("No articles found in the response.")
    return []


def save_to_csv(data: List, query: str, timestamp: Any) -> None:
    """
    Saves the extracted data to a CSV file with a category-based filename.

    Parameters:
        data (list): The list of articles to save.
        query (str): The query used to fetch the data.
        timestamp (str): Timestamp for unique file naming.
    """
    category = CATEGORY_MAP.get(query, "unknown")
    filename = f"{category}_{timestamp}.csv"
    file_path = os.path.join(DATA_DIR, filename)

    if not data:
        print(f"No data to save for query: {query}")
        return

    df = pd.json_normalize(data)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")


def main():
    """
    Main function to extract data and save it to CSV files for each search query.
    """
    if not IEEE_API_KEY:
        print("Error: IEEE API key not found. Make sure it's set in the .env file.")
        return 1

    for query in QUERIES:
        print(f"Fetching data for query: '{query}'")
        articles = fetch_papers(query)
        if articles:
            save_to_csv(
                articles, query, timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
            )


if __name__ == "__main__":
    main()
