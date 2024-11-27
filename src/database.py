#!/usr/bin/env python3

"""
"""

import sqlite3
import pandas as pd
import os
import config
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, name: str, filepath: Optional[str] = None):
        if filepath is None:
            self.db_name = f"{name}.db"
        else:
            self.db_name = os.path.join(filepath, f"{name}.db")
        self.connection = None

    @property
    def exists(self) -> bool:
        """
        Check if the database exists.

        Returns:
            bool: True if the database exists, False otherwise.
        """
        return os.path.exists(
            os.path.join(config.ROOT_DIR, config.DATA_DIR, self.db_name)
        )

    def initialize(self) -> None:
        """
        Initialize the database by creating required tables.
        """
        if self.exists():
            logger.error(f"Database '{self.db_name}' already exists.")
            raise AssertionError(f"Database '{self.db_name}' already exists.")

        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()

        # Create the main Papers table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS papers (
                paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
                is_number TEXT,
                insert_date DATE,
                publication_year INTEGER,
                download_count INTEGER,
                citing_patent_count INTEGER,
                title TEXT,
                abstract TEXT
            )
            """
        )

        # Create the Authors table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS authors (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id INTEGER,
                name TEXT,
                affiliation TEXT,
                FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
            )
            """
        )

        # Create the Index Terms table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS index_terms (
                index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id INTEGER,
                term_type TEXT,
                term TEXT,
                FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
            )
            """
        )

        # Create the Prompts table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prompts (
                prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id INTEGER,
                prompt_text TEXT,
                FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
            )
            """
        )

        self.connection.commit()
        logger.info(f"Database '{self.db_name}' initialized successfully.")

    @property
    def is_connected(self) -> bool:
        if self.connection is None:
            return False
        return True

    def connect(self) -> bool:
        """
        Connect to the database if not already connected.
        """
        if not self.is_connected:
            self.connection = sqlite3.connect(self.db_name)
        return self.connection is not None

    def push_df(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Push a DataFrame to a specific table in the database.

        Parameters:
            df (pd.DataFrame): The DataFrame to insert.
            table_name (str): The target table name.
        """
        self.connect()
        try:
            df.to_sql(table_name, self.connection, if_exists="append", index=False)
            logger.info(f"Data successfully inserted into '{table_name}'.")
        except Exception as e:
            logger.error(f"Failed to insert data into '{table_name}': {e}")
        finally:
            self.close()

    def query(self, query: str) -> pd.DataFrame:
        """
        Execute a query and return the results as a DataFrame.

        Parameters:
            query (str): The SQL query to execute.

        Returns:
            pd.DataFrame: The query results.
        """
        self.connect()
        return pd.read_sql_query(query, self.connection)

    def close(self) -> None:
        """
        Close the database connection.
        """
        if self.is_connected:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed.")
