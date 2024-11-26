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
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(ROOT_DIR, "data")
DATA_RAW_DIR = os.path.join(ROOT_DIR, "data/raw/")
DATA_PROCESSED_DIR = os.path.join(ROOT_DIR, "data/processed/")
DATA_CLASSIFIED_DIR = os.path.join(ROOT_DIR, "data/classified/")

# API Keys
IEEE_API_KEY = os.getenv("IEEE_API_KEY")

# Constants
BASE_URL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"

# Models
DEBERTA_V3_MODEL_NAME = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0"
