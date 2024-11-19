# IEEE Papers Mapper

## Overview

**IEEE Papers Mapper** is a tool that sources papers through the IEEE API and visualizes the results in a dashboard. The goal is to quantify and map research trends across various fields using intuitive visualizations.

## TODO

[X] Skeleton and Setup
[ ] Retrieve a research paper from IEEE API, make sure it's still compatible and all
[X] Create the idea of the end-goal. Is it a webapp or not?
[ ] Convert .ipynb files into .py files - Search what is a proper DS pipeline
[ ] Classify through context-aware embeddings (encoder-only transformers)
[ ] Idea RAG: premade texdt that will return based on similarity outcome. Maybe with a softmax and yes/no

## Features

- Automate data extraction from IEEE Xplore API.
- Clean and preprocess research data
- Classify research papers based on keywords or machine learning models
- Store data in a PostgreSQL (or SQLite) database
- Visualize research output using dynamic charts and graphs

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

1. Use SQLite instead of .CSV files for data storage.
