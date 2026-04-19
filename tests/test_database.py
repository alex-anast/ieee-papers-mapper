#!/usr/bin/env python3

import pytest
from ieee_papers_mapper.data.database import Database
from ieee_papers_mapper.data.repository import PaperRepository
from ieee_papers_mapper.models import ProcessedPaper, Author


@pytest.fixture
def db(tmp_path):
    db = Database(name="test_ieee_papers", filepath=str(tmp_path))
    db.initialise()
    return db


@pytest.fixture
def repo(db):
    return PaperRepository(db.connection)


@pytest.fixture
def sample_paper():
    return ProcessedPaper(
        is_number="99999",
        insert_date="2024-06-15",
        publication_year="2024",
        download_count=42,
        citing_patent_count=3,
        title="Deep Learning for Robotics",
        abstract="We propose a novel approach...",
        index_terms_ieee=["deep learning", "robotics"],
        index_terms_dynamic=["neural networks"],
        authors=[
            Author(author_id="100", full_name="Jane Smith", affiliation="MIT"),
            Author(author_id="101", full_name="John Doe", affiliation="Stanford"),
        ],
        prompt="title: Deep Learning for Robotics - abstract: We propose...",
    )


def test_create_tables(db):
    db.create_all_tables()
    existing_tables = db.get_existing_tables()
    assert "papers" in existing_tables
    assert "authors" in existing_tables
    assert "classification" in existing_tables


def test_insert_paper(repo):
    paper = ProcessedPaper(
        is_number="12345",
        insert_date="2024-01-01",
        publication_year="2023",
        download_count=10,
        citing_patent_count=2,
        title="Sample Paper",
        abstract="Sample Abstract",
        index_terms_ieee=[],
        index_terms_dynamic=[],
        authors=[],
        prompt="title: Sample Paper - abstract: Sample Abstract - index_terms: ",
    )
    paper_id = repo.insert_paper(paper)
    assert paper_id > 0
    result = repo.cursor.execute(
        "SELECT * FROM papers WHERE paper_id = ?", (paper_id,)
    ).fetchone()
    assert result[1] == "12345"


def test_insert_full_paper_round_trip(repo, sample_paper):
    repo.insert_full_paper(sample_paper)

    papers = repo.cursor.execute("SELECT * FROM papers").fetchall()
    assert len(papers) == 1
    assert papers[0][6] == "Deep Learning for Robotics"

    authors = repo.cursor.execute("SELECT name FROM authors ORDER BY name").fetchall()
    assert len(authors) == 2
    author_names = {row[0] for row in authors}
    assert "Jane Smith" in author_names
    assert "John Doe" in author_names

    index_terms = repo.cursor.execute("SELECT term FROM index_terms").fetchall()
    assert len(index_terms) == 3
    terms = {row[0] for row in index_terms}
    assert "deep learning" in terms
    assert "robotics" in terms
    assert "neural networks" in terms

    prompts = repo.cursor.execute("SELECT prompt_text FROM prompts").fetchall()
    assert len(prompts) == 1
    assert (
        prompts[0][0] == "title: Deep Learning for Robotics - abstract: We propose..."
    )


def test_paper_exists(repo, sample_paper):
    repo.insert_full_paper(sample_paper)
    assert repo.paper_exists("99999") is True
    assert repo.paper_exists("00000") is False


def test_duplicate_paper_skipped(repo, sample_paper):
    repo.insert_full_paper(sample_paper)
    repo.insert_full_paper(sample_paper)
    count = repo.cursor.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    assert count == 1


def test_close_and_reconnect(db):
    db.close()
    assert db.is_connected is False
    db.connect()
    assert db.is_connected is True
