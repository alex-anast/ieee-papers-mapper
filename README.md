# IEEE Papers Mapper

## Overview

**IEEE Papers Mapper** is a tool that sources papers through the IEEE API and visualizes the results in a dashboard. The goal is to quantify and map research trends across various fields using intuitive visualizations.

## TODO

- [ ] Automate data retrieval (chron or APScheduler)
- [ ] Automate, classify, store in the DB
- [ ] For the dash webapp, create a prototype interactive interface
- [ ] If webapp is running, if a change in the database has happened, let the user know through a push notification and update visuals
- [ ] Try and connect everything together!

## Features

- Automate data extraction from IEEE Xplore API.
- Clean and preprocess research data
- Classify research papers based on keywords or machine learning models
- Store data in a PostgreSQL (or SQLite) database
- Visualize research output using dynamic charts and graphs

## Repo Structure Logic

```bash
src/
├── app/                        # Web application
│   ├── __init__.py             # Initializes the app as a package
│   ├── dash_webapp.py          # Dash application logic
│   ├── callbacks.py            # Callbacks for interactivity
│   └── assets/                 # Static files (CSS, images, etc.)
│       └── styles.css
│
├── config/                     # Configuration and environment setup
│   ├── config.py               # Contains constants, model names, API keys
│   └── scheduler.py            # Scheduler setup (APScheduler logic)
│
├── data/                       # Data processing and classification
│   ├── get_papers.py           # Fetch data from IEEE API
│   ├── process_papers.py       # Preprocess raw data
│   ├── classify_papers.py      # Classify papers
│   ├── pipeline.py             # End-to-end pipeline logic
│   ├── database.py             # Database setup and query functions
│   └── demo.ipynb              # Demo notebook for testing workflows
│
├── main.py                     # Main script orchestrating the phases
└── __init__.py                 # Initializes the src directory as a package
tests/                          # Testing
├── test_database.py            # Unit tests for database module
├── test_classify_papers.py     # Unit tests for classification
└── test_end_to_end.py          # End-to-end workflow tests
```

## Project Structure / Steps

Outline what this teaches you for future recruiters!

1. Data Collection
    - IEEE API Integration (`requests`, pagination)
    - Data Storage (JSON, CSV, SQLite, Data Version Control (DVC))
    - Data Cleaning (removal, normalization, tokenization)
    - Preprocessing (matadata)
2. Text Classification (Keyword classification, LLMs, Embedding (Semantic) Search)
3. Trend Analysis & Visualization
4. Deployment & Documentation
    - Web deployment
    - `docs/` folder, and `notebooks/` folder for tutorial

## Getting Started

### Prerequisites

### Installation

### Usage

## Workflow

## Classifiers

## Contributions

## License

## Contact

## Future Ideas

- Get geolocation of the cities and have a map-like dashboard

