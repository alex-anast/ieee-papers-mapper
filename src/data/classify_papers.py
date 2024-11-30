#!/usr/bin/env python3

import config.config as cfg
import pandas as pd
from transformers import pipeline


classifier = pipeline("zero-shot-classification", model=cfg.DEBERTA_V3_MODEL_NAME)


def classify_text(text: str) -> list:
    """
    Classify a single text into multiple categories.

    Parameters:
        text (str): The input text to classify.

    Returns:
        list: A list of tuples (category, confidence).
    """
    results = classifier(text, candidate_labels=cfg.CATEGORIES, multi_label=True)
    return [
        (label, score) for label, score in zip(results["labels"], results["scores"])
    ]


def classify_all_papers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify all papers and return their classifications.

    Parameters:
        df (pd.DataFrame): DataFrame with `paper_id` and `prompt_text`.

    Returns:
        pd.DataFrame: DataFrame with `paper_id`, `category`, and `confidence`.
    """
    classifications = []
    for _, row in df.iterrows():
        classifications.extend(
            [
                {"paper_id": row["paper_id"], "category": cat, "confidence": conf}
                for cat, conf in classify_text(row["prompt_text"])
            ]
        )
    return pd.DataFrame(classifications)
