#!/usr/bin/env python3

"""
"""

import sqlite3
import pandas as pd

DB_PATH = "./data/ieee_papers.db"


def initialize_database():
    """
    Initializes the SQLite database and creates necessary tables if they don't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table for storing papers
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            abstract TEXT,
            category TEXT,
            confidence REAL,
            publication_year INTEGER,
            processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def insert_classified_data(file_path):
    """
    Inserts classified data from a CSV file into the SQLite database.

    Parameters:
        file_path (str): Path to the classified CSV file.
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        conn.execute(
            """
            INSERT INTO papers (title, abstract, category, confidence, publication_year)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                row["title"],
                row["abstract"],
                row["category"],
                row["confidence"],
                row["publication_year"],
            ),
        )

    conn.commit()
    conn.close()
    print(f"Data from {file_path} inserted into the database.")


def query_papers(category=None):
    """
    Queries papers from the database by category.

    Parameters:
        category (str): The category to filter by (optional).

    Returns:
        list: A list of rows matching the query.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if category:
        cursor.execute("SELECT * FROM papers WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM papers")

    rows = cursor.fetchall()
    conn.close()
    return rows
