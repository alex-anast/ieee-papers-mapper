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
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

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

    def paper_exists(self, is_number: str) -> bool:
        """
        Check if a paper with the given is_number exists in the database.

        Parameters:
            is_number (str): Unique identifier for the paper.

        Returns:
            bool: True if the paper exists, False otherwise.
        """
        query = "SELECT 1 FROM papers WHERE is_number = ?"
        self.cursor.execute(query, (is_number,))
        return self.cursor.fetchone() is not None

    def insert_paper(self, paper_data: dict) -> int:
        """
        Insert a paper into the papers table and return its paper_id.

        Parameters:
            paper_data (dict): Dictionary containing paper metadata.

        Returns:
            int: The paper_id of the inserted paper.
        """
        query = """
        INSERT INTO papers (is_number, insert_date, publication_year, download_count,
                            citing_patent_count, title, abstract)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            paper_data['is_number'],
            paper_data['insert_date'],
            paper_data['publication_year'],
            paper_data['download_count'],
            paper_data['citing_patent_count'],
            paper_data['title'],
            paper_data['abstract'],
        ))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_authors(self, paper_id: int, authors: list):
        """
        Insert authors into the authors table.

        Parameters:
            paper_id (int): The ID of the associated paper.
            authors (list): List of dictionaries containing author data.
        """
        query = """
        INSERT INTO authors (paper_id, name, affiliation)
        VALUES (?, ?, ?)
        """
        for author in authors:
            self.cursor.execute(query, (paper_id, author['author_full_name'], author['author_affiliation']))
        self.connection.commit()

    def insert_index_terms(self, paper_id: int, term_type: str, terms: list):
        """
        Insert index terms into the index_terms table.

        Parameters:
            paper_id (int): The ID of the associated paper.
            term_type (str): The type of index term (e.g., 'author', 'ieee', 'dynamic').
            terms (list): List of terms.
        """
        query = """
        INSERT INTO index_terms (paper_id, term_type, term)
        VALUES (?, ?, ?)
        """
        for term in terms:
            self.cursor.execute(query, (paper_id, term_type, term))
        self.connection.commit()

    def insert_prompt(self, paper_id: int, prompt: str):
        """
        Insert a prompt into the prompts table.

        Parameters:
            paper_id (int): The ID of the associated paper.
            prompt (str): The prompt text.
        """
        query = "INSERT INTO prompts (paper_id, prompt_text) VALUES (?, ?)"
        self.cursor.execute(query, (paper_id, prompt))
        self.connection.commit()

    def insert_full_paper(self, row: pd.Series):
        """
        Insert a full paper, including all related data, into the database.

        Parameters:
            row (pd.Series): A row from the processed DataFrame.
        """
        if self.paper_exists(row['is_number']):
            print(f"Paper with is_number {row['is_number']} already exists. Skipping.")
            return

        # Insert main paper metadata
        paper_data = row[['is_number', 'insert_date', 'publication_year', 'download_count',
                          'citing_patent_count', 'title', 'abstract']].to_dict()
        paper_id = self.insert_paper(paper_data)

        # Insert authors
        authors = row['authors']
        self.insert_authors(paper_id, authors)

        # Insert index terms
        index_terms_types = ['author', 'ieee', 'dynamic']
        index_terms_columns = ['index_terms_author', 'index_terms_ieee', 'index_terms_dynamic']
        for term_type, terms_column in zip(index_terms_types, index_terms_columns):
            terms = row[terms_column]
            self.insert_index_terms(paper_id, term_type, terms)

        # Insert prompt
        self.insert_prompt(paper_id, row['prompt'])
