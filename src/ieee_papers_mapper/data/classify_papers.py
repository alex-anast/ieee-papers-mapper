#!/usr/bin/env python3

import time
import pandas as pd
import logging
from ieee_papers_mapper.config import config as cfg
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


def classify_text(text: str, timer: bool = False) -> list:
    """
    Classify a single text into multiple categories.

    Parameters:
        text (str): The input text to classify.

    Returns:
        list: A list of tuples (category, confidence).
    """
    if timer:
        start_time = time.time()

    results = _get_classifier()(text, candidate_labels=cfg.CATEGORIES, multi_label=True)

    if timer:
        elapsed_time = time.time() - start_time
        logger.debug(f"Paper's classification time: {elapsed_time:.2f}s")

    return [
        (label, score) for label, score in zip(results["labels"], results["scores"])
    ]


def classify_all_papers(df: pd.DataFrame, timer: bool = False) -> list[ClassifiedPaper]:
    """
    Classify all papers and return their classifications.

    Parameters:
        df (pd.DataFrame): DataFrame with `paper_id` and `prompt_text`.

    Returns:
        list[ClassifiedPaper]: List of ClassifiedPaper models.
    """
    classifications = []
    times = []
    for _, row in df.iterrows():
        if timer:
            start_time = time.time()
        for cat, conf in classify_text(row["prompt_text"]):
            classifications.append(
                ClassifiedPaper(paper_id=row["paper_id"], category=cat, confidence=conf)
            )
        if timer:
            elapsed_time = time.time() - start_time
            times.append(elapsed_time)
    if timer and times:
        mean_classification_time = sum(times) / len(times)
        logger.debug(f"Mean Paper Classification Time: {mean_classification_time:.2f}s")
        logger.debug(f"Total Elapsed Classification Time: {sum(times):.2f}s")
    return classifications
