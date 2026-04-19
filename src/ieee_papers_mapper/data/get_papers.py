#!/usr/bin/env python3

"""
IEEE Papers Data Extraction Script
==================================
This script retrieves research papers from the IEEE Xplore API based on a specified query.

Features:
- Fetch papers from the IEEE Xplore API.
- Handle API errors by raising IEEEApiError.
- Return an empty DataFrame when no results are found.

Dependencies:
- Requests for API calls.
- Pandas for data manipulation.
"""

import requests
import pandas as pd
import logging
from ieee_papers_mapper.config import config as cfg
from ieee_papers_mapper.exceptions import IEEEApiError

logger = logging.getLogger("ieee_logger")


def get_papers(
    query: str,
    start_year: str,
    api_key: str,
    max_records: int,
    start_record: int,
) -> pd.DataFrame:
    params = {
        "apikey": api_key,
        "format": "json",
        "content_type": "Journals",
        "start_year": start_year,
        "max_records": max_records,
        "sort_field": "article_number",
        "sort_order": "asc",
        "querytext": query,
        "start_record": start_record,
    }

    try:
        response = requests.get(cfg.BASE_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise IEEEApiError(f"API request failed for query '{query}': {e}") from e

    papers = response.json().get("articles", [])
    if not papers:
        logger.info(f"No data fetched for query: {query}")
        return pd.DataFrame()

    df = pd.json_normalize(papers)
    logger.info(f"Successfully fetched {len(df)} articles for query: {query}")
    return df
