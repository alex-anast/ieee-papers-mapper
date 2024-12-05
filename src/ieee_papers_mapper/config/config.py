#!/usr/bin/env python3

"""
What:
    Contains all constants ang global variables.

Why:
    - Easy to access and modify centralized configurations.
    - Keeps configuration logic separate from the rest of the implementation.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Directories
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
SRC_DIR = os.path.join(ROOT_DIR, "ieee_papers_mapper")
CONFIG_DIR = os.path.join(SRC_DIR, "config")
JSON_FILENAME = "progress.json"
DB_PATH = os.path.join(SRC_DIR, "ieee_papers.db")

# IEEE API Parameters
IEEE_API_KEY = os.getenv("IEEE_API_KEY")
IEEE_API_START_RECORD = 1
IEEE_API_START_YEAR = 2024
# TODO: Change to 200
IEEE_API_MAX_RECORDS = 20

# Constants
BASE_URL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
CATEGORIES = ["machine learning", "power electronics", "robotics"]
DB_TABLES = ["papers", "authors", "index_terms", "prompts", "classification"]

# Models
DEBERTA_V3_MODEL_NAME = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0"
