#!/usr/bin/env python3

"""
IEEE Papers Data Extraction Script
=================================
This script fetches research papers from the IEEE Xplore API based on specific search queries.
It saves the extracted data in a CSV format for further analysis.

Usage:
    python data_extraction.py

Requirements:
    - requests
    - pandas
    - python-dotenv (for environment variable management)

Make sure to set your IEEE API key in a `.env` file as follows:
    IEEE_API_KEY=your_api_key_here
"""

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
IEEE_API_KEY = os.getenv("IEEE_API_KEY")

# Constants
BASE_URL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
DATA_DIR = "./data/raw/"
META_DATA = [
    "onboard charger OR on-board charger OR integrated charger",
    "dc-dc converter OR dc/dc converter",
    "inverter OR dc/ac converter OR dc-ac converter",
    "gallium nitride",
    "silicon carbide",
]


def fetch_papers(query: str, start_year: str = "2020", max_records: int = 10):
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
        response = response.json().get("articles", [])
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error during requests to {BASE_URL}: {req_err}")
    except KeyError:
        print("No articles found in the response.")
    return []


def save_to_csv(data, filename):
    """
    Saves the extracted data to a CSV file.

    Parameters:
        data (list): The list of articles to save.
        filename (str): The filename for the CSV file.
    """
    if not data:
        print("No data to save.")
        return

    df = pd.json_normalize(data)
    os.makedirs(DATA_DIR, exist_ok=True)

    file_path = os.path.join(DATA_DIR, filename)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")


def main():
    """
    Main function to extract data and save it to CSV files for each search query.
    """
    if not IEEE_API_KEY:
        print("Error: IEEE API key not found. Make sure it's set in the .env file.")
        return 1

    for query in META_DATA:
        print(f"Fetching data for query: '{query}'")
        articles = fetch_papers(query)
        if articles:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{query.replace(' ', '_')}_{timestamp}.csv"
            save_to_csv(articles, filename)


if __name__ == "__main__":
    main()
