#!/usr/bin/env python3

"""
IEEE Papers Data Extraction Script
==================================
This script fetches research papers from the IEEE Xplore API based on a specific search query.
The query and optional file name are provided as command-line arguments.
"""

import requests
import pandas as pd
import argparse
import config.config as cfg
import logging
from typing import Optional

logger = logging.getLogger("ieee_logger")


def get_papers(query: str, start_year: str, max_records: int) -> Optional[pd.DataFrame]:
    """
    Gets research papers from the IEEE API.

    Parameters:
        query (str): The search query for the API.
        start_year (str): The starting year for the search.
        max_records (int): Maximum number of records to fetch (max 200).

    Returns:
        list: A list of articles retrieved from the API.
    """
    params = {
        "apikey": cfg.IEEE_API_KEY,
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
        response = requests.get(cfg.BASE_URL, params=params)
        response.raise_for_status()
        papers = response.json().get("articles", [])
        if not papers:
            logger.info(f"TERMINATE: No data fetched for query:\n    {query}")
            return None

        # Convert the list of articles to a DataFrame
        df = pd.json_normalize(papers)
        logger.info(f"Successfully fetched {len(df)} articles for query: {query}")
        return df

    except requests.exceptions.HTTPError as http_err:
        logger.warning(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.warning(f"Error during requests to {cfg.BASE_URL}: {req_err}")
    except KeyError:
        logger.warning("No articles found in the response.")
    return []


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
