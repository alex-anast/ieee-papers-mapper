#!/usr/bin/env python3

import time
import pandas as pd
import logging
from ieee_papers_mapper.config import config as cfg
from ieee_papers_mapper.config.metrics import classification_latency, papers_classified
from ieee_papers_mapper.models import ClassifiedPaper

logger = logging.getLogger("ieee_logger")

_classifier = None


def _get_classifier():
    global _classifier
    if _classifier is None:
        from transformers import pipeline as hf_pipeline

        _classifier = hf_pipeline(
            "zero-shot-classification", model=cfg.DEBERTA_V3_MODEL_NAME
        )
    return _classifier


def classify_text(text: str) -> list:
    """
    Classify a single text into multiple categories.

    Parameters:
        text (str): The input text to classify.

    Returns:
        list: A list of tuples (category, confidence).
    """
    results = _get_classifier()(text, candidate_labels=cfg.CATEGORIES, multi_label=True)
    return [
        (label, score) for label, score in zip(results["labels"], results["scores"])
    ]


def classify_all_papers(df: pd.DataFrame) -> list[ClassifiedPaper]:
    """
    Classify all papers and return their classifications.

    Parameters:
        df (pd.DataFrame): DataFrame with `paper_id` and `prompt_text`.

    Returns:
        list[ClassifiedPaper]: List of ClassifiedPaper models.
    """
    classifications = []
    for _, row in df.iterrows():
        start = time.monotonic()
        for cat, conf in classify_text(row["prompt_text"]):
            classifications.append(
                ClassifiedPaper(paper_id=row["paper_id"], category=cat, confidence=conf)
            )
            papers_classified.labels(category=cat).inc()
        classification_latency.observe(time.monotonic() - start)
    return classifications
