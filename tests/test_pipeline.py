#!/usr/bin/env python3

import os
import json
import duckdb
import pytest
import pandas as pd
from unittest.mock import patch
from ieee_papers_mapper.models import ClassifiedPaper
from ieee_papers_mapper.data.pipeline import run_pipeline, load_progress, save_progress


def test_load_progress_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr("ieee_papers_mapper.config.config.CONFIG_DIR", str(tmp_path))
    result = load_progress("nonexistent.json")
    assert result == {}


def test_load_and_save_progress_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr("ieee_papers_mapper.config.config.CONFIG_DIR", str(tmp_path))
    progress = {"machine learning": 201}
    save_progress("progress.json", progress)
    loaded = load_progress("progress.json")
    assert loaded == {"machine learning": 201}


def test_run_pipeline_with_new_papers(tmp_path, monkeypatch):
    monkeypatch.setattr("ieee_papers_mapper.config.config.SRC_DIR", str(tmp_path))
    monkeypatch.setattr("ieee_papers_mapper.config.config.CONFIG_DIR", str(tmp_path))
    monkeypatch.setattr(
        "ieee_papers_mapper.config.config.CATEGORIES", ["test category"]
    )
    monkeypatch.setattr("ieee_papers_mapper.config.config.IEEE_API_MAX_RECORDS", 50)

    mock_api_response = pd.DataFrame(
        {
            "is_number": ["12345"],
            "insert_date": ["20240615"],
            "publication_year": ["2024"],
            "download_count": [42],
            "citing_patent_count": [3],
            "title": ["Test Paper Title"],
            "abstract": ["Test abstract content"],
            "index_terms.ieee_terms.terms": ['["deep learning", "neural networks"]'],
            "index_terms.dynamic_index_terms.terms": ['["AI"]'],
            "authors.authors": [
                '[{"id": "1", "full_name": "Test Author", "affiliation": "Test University"}]'
            ],
        }
    )

    mock_classification_result = [
        ClassifiedPaper(paper_id=1, category="machine learning", confidence=0.92)
    ]

    with (
        patch(
            "ieee_papers_mapper.data.pipeline.get_papers",
            side_effect=[mock_api_response, pd.DataFrame()],
        ),
        patch(
            "ieee_papers_mapper.data.pipeline.classify_all_papers",
            return_value=mock_classification_result,
        ),
    ):
        result = run_pipeline()

    assert result is True

    db_path = str(tmp_path / "ieee_papers.duckdb")
    conn = duckdb.connect(db_path, read_only=True)
    cursor = conn.cursor()

    paper_count = cursor.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    assert paper_count == 1

    title = cursor.execute("SELECT title FROM papers").fetchone()[0]
    assert title == "Test Paper Title"

    author_count = cursor.execute("SELECT COUNT(*) FROM authors").fetchone()[0]
    assert author_count == 1

    prompt_count = cursor.execute("SELECT COUNT(*) FROM prompts").fetchone()[0]
    assert prompt_count == 1

    classification_count = cursor.execute(
        "SELECT COUNT(*) FROM classification"
    ).fetchone()[0]
    assert classification_count == 1

    category, confidence = cursor.execute(
        "SELECT category, confidence FROM classification"
    ).fetchone()
    assert category == "machine learning"
    assert abs(confidence - 0.92) < 1e-6

    conn.close()

    progress_path = tmp_path / "progress.json"
    assert progress_path.exists()
    with open(str(progress_path)) as f:
        saved_progress = json.load(f)
    assert "test category" in saved_progress
    assert saved_progress["test category"] == 51  # 1 + IEEE_API_MAX_RECORDS (50)


def test_run_pipeline_no_new_papers(tmp_path, monkeypatch):
    monkeypatch.setattr("ieee_papers_mapper.config.config.SRC_DIR", str(tmp_path))
    monkeypatch.setattr("ieee_papers_mapper.config.config.CONFIG_DIR", str(tmp_path))
    monkeypatch.setattr(
        "ieee_papers_mapper.config.config.CATEGORIES", ["test category"]
    )
    monkeypatch.setattr("ieee_papers_mapper.config.config.IEEE_API_MAX_RECORDS", 50)

    with (
        patch(
            "ieee_papers_mapper.data.pipeline.get_papers",
            return_value=pd.DataFrame(),
        ),
        patch(
            "ieee_papers_mapper.data.pipeline.classify_all_papers",
        ) as mock_classify,
    ):
        result = run_pipeline()

    assert result is False
    mock_classify.assert_not_called()
