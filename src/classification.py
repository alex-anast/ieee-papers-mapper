#!/usr/bin/env python3

"""
"""

import os
import pandas as pd
from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification, pipeline

# Directory paths
PROCESSED_DATA_DIR = "./data/processed/"
CLASSIFIED_DATA_DIR = "./data/classified/"

# Categories and labels
# This goes into the query. For that reason, treat it like one.
# Example: Inverters OR AC-DC Converters
# TODO: Change the `None of the above` to an intelligent query,
#           after experimentation it is shown that it is needed.
CATEGORIES = [
    "DC-DC converters",
    "Inverters",
    "On-board chargers",
    "Gallium Nitride transistors",
    "Silicon Carbide transistors",
    "None of the above",  # Default category
]

# deBERTa-v3 models
MODEL_NAME = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0"

classifier = pipeline("zero-shot-classification", model=MODEL_NAME)

def classify_text(text):
    """
    Classifies a single text into one of the predefined categories.

    Parameters:
        text (str): The input text to classify.

    Returns:
        tuple: Best category and its confidence score.
    """
    results = classifier(text, candidate_labels=CATEGORIES, multi_label=False)
    # Find the label with the highest score
    best_index = results["scores"].index(max(results["scores"]))
    best_category = results["labels"][best_index]
    best_score = results["scores"][best_index]
    return best_category, best_score

def classify_papers(input_file: str, output_dir: str) -> None:
    """
    Classifies research papers from a preprocessed CSV file into predefined categories.

    Parameters:
        input_file (str): Path to the preprocessed CSV file.
        output_dir (str): Directory where the classified file will be saved.
    """
    # Load the preprocessed data
    df = pd.read_csv(input_file)

    # Apply the classification to each row (~20s per entry)
    df["category"], df["confidence"] = zip(*df["text_input"].apply(classify_text))

    # Save the classified data
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    df.to_csv(output_file, index=False)
    print(f"Classified data saved to: {output_file}")

if __name__ == "__main__":
    classify_papers(
        input_file=os.path.join(PROCESSED_DATA_DIR, "obc.csv"),
        output_dir=CLASSIFIED_DATA_DIR,
    )
