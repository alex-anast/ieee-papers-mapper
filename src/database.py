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
    def __init__(self, name: str, filepath: Optional[str]=None):
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
        if self.exists:
            logger.error(f"Database '{self.db_name}' already exists.")
            raise AssertionError

        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()

        # Create tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS raw_papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                abstract TEXT,
                publication_year INTEGER,
                raw_data TEXT,
                processed BOOLEAN DEFAULT FALSE,
                classified BOOLEAN DEFAULT FALSE
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS classified_papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_paper_id INTEGER,
                category TEXT,
                confidence REAL,
                processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(raw_paper_id) REFERENCES raw_papers(id)
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
        self.connect() if self.is_connected is False else None
        df.to_sql(table_name, self.connection, if_exists="append", index=False)
        logger.info(f"Data pushed to table '{table_name}' successfully.")

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
