#!/usr/bin/env python3


"""
Database Module for IEEE Papers Mapper
======================================

This module manages the DuckDB database used by the IEEE Papers Mapper project.
It is responsible for connection management and schema initialisation only.
All CRUD operations are handled by PaperRepository in repository.py.

Classes:
    Database: Manages the database connection lifecycle and table creation.

Functions:
    - initialise: Creates tables in the database if they don't exist.
    - create_all_tables: Creates all expected tables from scratch.
    - create_tables: Creates a specified subset of tables.
    - connect: Opens a connection to the database.
    - close: Closes the active database connection.
"""


import os
import duckdb
import logging
from typing import Optional
from ieee_papers_mapper.config import config as cfg

logger = logging.getLogger("ieee_logger")


class Database:
    """Connection and schema manager for the IEEE Papers DuckDB database."""

    def __init__(self, name: str, filepath: Optional[str] = None):
        if filepath is None:
            self.db_name = f"{name}.duckdb"
        else:
            self.db_name = os.path.join(filepath, f"{name}.duckdb")
        self.connection = duckdb.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.expected_tables = cfg.DB_TABLES

    @property
    def file_exists(self) -> bool:
        return os.path.exists(os.path.join(cfg.SRC_DIR, self.db_name))

    def get_existing_tables(self):
        if not self.file_exists:
            return []
        conn = duckdb.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        )
        existing_tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return existing_tables

    def initialise(self):
        if not self.file_exists:
            logger.info("Database file doesn't exist, creating from scratch...")
            self.create_all_tables()
        else:
            existing_tables = self.get_existing_tables()
            missing_tables = set(self.expected_tables) - set(existing_tables)
            logger.info(
                f"Database file exists, creating missing tables: {missing_tables}"
            )
            if missing_tables:
                self.create_tables(missing_tables)

    def create_all_tables(self):
        conn = duckdb.connect(self.db_name)
        cursor = conn.cursor()
        self.create_tables(self.expected_tables, cursor)
        conn.commit()
        conn.close()

    def create_tables(self, tables, cursor=None):
        if cursor is None:
            conn = duckdb.connect(self.db_name)
            cursor = conn.cursor()
        else:
            conn = None

        ordered_tables = [t for t in self.expected_tables if t in tables]
        for table in ordered_tables:
            if table == "papers":
                cursor.execute("CREATE SEQUENCE IF NOT EXISTS papers_id_seq")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS papers (
                        paper_id INTEGER PRIMARY KEY DEFAULT nextval('papers_id_seq'),
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
            elif table == "authors":
                cursor.execute("CREATE SEQUENCE IF NOT EXISTS authors_id_seq")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS authors (
                        author_id INTEGER PRIMARY KEY DEFAULT nextval('authors_id_seq'),
                        paper_id INTEGER,
                        name TEXT,
                        affiliation TEXT,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                """
                )
            elif table == "index_terms":
                cursor.execute("CREATE SEQUENCE IF NOT EXISTS index_terms_id_seq")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS index_terms (
                        index_id INTEGER PRIMARY KEY DEFAULT nextval('index_terms_id_seq'),
                        paper_id INTEGER,
                        term_type TEXT,
                        term TEXT,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                """
                )
            elif table == "prompts":
                cursor.execute("CREATE SEQUENCE IF NOT EXISTS prompts_id_seq")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS prompts (
                        prompt_id INTEGER PRIMARY KEY DEFAULT nextval('prompts_id_seq'),
                        paper_id INTEGER,
                        prompt_text TEXT,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                """
                )
            elif table == "classification":
                cursor.execute("CREATE SEQUENCE IF NOT EXISTS classification_id_seq")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS classification (
                        classification_id INTEGER PRIMARY KEY DEFAULT nextval('classification_id_seq'),
                        paper_id INTEGER,
                        category TEXT,
                        confidence REAL,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                """
                )

        if conn:
            conn.commit()
            conn.close()
            logger.info(f"Database '{self.db_name}' initialised successfully.")

    @property
    def is_connected(self) -> bool:
        if self.connection is None:
            return False
        return True

    def connect(self) -> bool:
        if not self.is_connected:
            self.connection = duckdb.connect(self.db_name)
        return self.connection is not None

    def close(self) -> None:
        if self.is_connected:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed.")
