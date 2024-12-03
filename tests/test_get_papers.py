#!/usr/bin/env python3

import pytest
import requests
import pandas as pd
from ..ieee_papers_mapper.data.get_papers import get_papers


@pytest.fixture
def mock_response():
    return {
        "articles": [
            {"title": "Paper 1", "abstract": "Abstract 1"},
            {"title": "Paper 2", "abstract": "Abstract 2"},
        ]
    }


def test_get_papers_success(mock_response, requests_mock):
    query = "machine learning"
    requests_mock.get(
        "https://ieeexploreapi.ieee.org/api/v1/search/articles", json=mock_response
    )

    df = get_papers(
        query=query,
        start_year="2020",
        api_key="dummy_key",
        max_records=2,
        start_record=1,
    )
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 2


def test_get_papers_no_data(requests_mock):
    query = "nonexistent topic"
    requests_mock.get(
        "https://ieeexploreapi.ieee.org/api/v1/search/articles", json={"articles": []}
    )

    df = get_papers(
        query=query,
        start_year="2020",
        api_key="dummy_key",
        max_records=2,
        start_record=1,
    )
    assert df is None


def test_get_papers_request_exception(requests_mock):
    query = "machine learning"
    requests_mock.get(
        "https://ieeexploreapi.ieee.org/api/v1/search/articles",
        exc=requests.exceptions.RequestException,
    )

    df = get_papers(
        query=query,
        start_year="2020",
        api_key="dummy_key",
        max_records=2,
        start_record=1,
    )
    assert df is None
