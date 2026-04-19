#!/usr/bin/env python3

import pytest
import pandas as pd
from ieee_papers_mapper.models import ProcessedPaper, Author
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
        "index_terms.ieee_terms.terms": ['["term3", "term4"]'],
        "index_terms.dynamic_index_terms.terms": ['["term5"]'],
        "authors.authors": [
            '[{"id": "1", "full_name": "Author 1", "affiliation": "Affiliation 1"}]'
        ],
    }
    return pd.DataFrame(data)


def test_process_papers(sample_raw_data):
    papers = process_papers(sample_raw_data)
    assert len(papers) == 1
    assert isinstance(papers[0], ProcessedPaper)
    assert papers[0].title == "Sample Title"
    assert papers[0].prompt.startswith("title: Sample Title")
    assert papers[0].insert_date == "2024-01-01"


def test_safe_parse_list_valid():
    result = _safe_parse_list('["term1", "term2"]')
    assert result == ["term1", "term2"]


def test_safe_parse_list_invalid():
    result = _safe_parse_list("not a list")
    assert result == []


def test_safe_parse_list_non_string():
    result = _safe_parse_list(None)
    assert result == []


def test_safe_parse_list_already_parsed():
    result = _safe_parse_list(["term1", "term2"])
    assert result == ["term1", "term2"]


def test_extract_author_info():
    authors_str = '[{"id": "1", "full_name": "Alice", "affiliation": "MIT"}]'
    result = _extract_author_info(authors_str)
    assert len(result) == 1
    assert isinstance(result[0], Author)
    assert result[0].full_name == "Alice"
    assert result[0].affiliation == "MIT"
    assert result[0].author_id == "1"


def test_create_prompt():
    result = _create_prompt("Test Title", "Test Abstract", ["term1"], ["term2"])
    assert (
        result
        == "title: Test Title - abstract: Test Abstract - index_terms: term1, term2"
    )
