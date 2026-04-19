#!/usr/bin/env python3

import pytest
import pandas as pd
from ieee_papers_mapper.models import ClassifiedPaper
from ieee_papers_mapper.data.classify_papers import (
    classify_text,
    classify_all_papers,
)


@pytest.fixture
def mock_prompt_data():
    data = {"paper_id": [1], "prompt_text": ["Sample Title and Abstract"]}
    return pd.DataFrame(data)


def test_classify_text(mocker):
    mock_classifier = mocker.MagicMock(
        return_value={"labels": ["Category 1", "Category 2"], "scores": [0.9, 0.1]}
    )
    mocker.patch(
        "ieee_papers_mapper.data.classify_papers._get_classifier",
        return_value=mock_classifier,
    )
    result = classify_text("Sample prompt")
    assert result[0][0] == "Category 1"
    assert result[0][1] == 0.9


def test_classify_all_papers(mock_prompt_data, mocker):
    mocker.patch(
        "ieee_papers_mapper.data.classify_papers.classify_text",
        return_value=[("Category 1", 0.95)],
    )
    result = classify_all_papers(mock_prompt_data)
    assert len(result) == 1
    assert isinstance(result[0], ClassifiedPaper)
    assert result[0].category == "Category 1"
    assert result[0].confidence == 0.95
