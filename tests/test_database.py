#!/usr/bin/env python3

import pytest
from ..ieee_papers_mapper.data.database import Database


@pytest.fixture
def db():
    db = Database(name="test_db")
    db.initialize()
    yield db
    db.close()


def test_create_tables(db):
    existing_tables = db.get_existing_tables()
    assert "papers" in existing_tables
    assert "authors" in existing_tables
    assert "classification" in existing_tables


def test_insert_paper(db):
    paper_data = {
        "is_number": "12345",
        "insert_date": "2024-01-01",
        "publication_year": "2023",
        "download_count": 10,
        "citing_patent_count": 2,
        "title": "Sample Paper",
        "abstract": "Sample Abstract",
    }
    paper_id = db.insert_paper(paper_data)
    assert paper_id > 0
    result = db.cursor.execute(
        "SELECT * FROM papers WHERE paper_id = ?", (paper_id,)
    ).fetchone()
    assert result[1] == "12345"
