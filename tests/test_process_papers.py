#!/usr/bin/env python3

import pytest
import pandas as pd
from ieee_papers_mapper.data.process_papers import (
    process_papers,
    _safe_parse_list,
    _extract_author_info,
    _create_prompt,
)


@pytest.fixture
def sample_raw_data():
    data = {
        "is_number": ["12345"],
        "insert_date": ["20240101"],
        "publication_year": ["2020"],
        "download_count": [10],
        "citing_patent_count": [2],
        "title": ["Sample Title"],
        "abstract": ["Sample Abstract"],
        # "index_terms.author_terms.terms": ['["term1", "term2"]'],
        "index_terms.ieee_terms.terms": ['["term3", "term4"]'],
        "index_terms.dynamic_index_terms.terms": ['["term5"]'],
        "authors.authors": [
            '[{"id": "1", "full_name": "Author 1", "affiliation": "Affiliation 1"}]'
        ],
    }
    return pd.DataFrame(data)


def test_process_papers(sample_raw_data):
    df_processed = process_papers(sample_raw_data)
    assert "prompt" in df_processed.columns
    assert df_processed["prompt"].iloc[0].startswith("title: Sample Title")
    # assert df_processed["index_terms_author"].iloc[0] == ["term1", "term2"]


def test_safe_parse_list_valid():
    result = _safe_parse_list('["term1", "term2"]')
    assert result == ["term1", "term2"]


def test_safe_parse_list_invalid():
    result = _safe_parse_list("not a list")
    assert result == []


def test_safe_parse_list_non_string():
    result = _safe_parse_list(None)
    assert result == []


def test_extract_author_info():
    authors_str = '[{"id": "1", "full_name": "Alice", "affiliation": "MIT"}]'
    result = _extract_author_info(authors_str)
    assert result == [
        {"author_id": "1", "author_full_name": "Alice", "author_affiliation": "MIT"}
    ]


def test_create_prompt():
    row = pd.Series(
        {
            "title": "Test Title",
            "abstract": "Test Abstract",
            "index_terms_ieee": ["term1"],
            "index_terms_dynamic": ["term2"],
        }
    )
    result = _create_prompt(row)
    assert (
        result
        == "title: Test Title - abstract: Test Abstract - index_terms: term1, term2"
    )
