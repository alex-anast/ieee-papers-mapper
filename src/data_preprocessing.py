#!/usr/bin/env python3

"""

"""


import os
import pandas as pd
import config
from typing import List


def import_csv(file_path: str, column_selection: List = None) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df[column_selection]


def preprocess_csv(file_path: str, output_dir: str) -> None:
    """
    Preprocess a single CSV file to retain relevant information for classification.

    Columns of interest:
        ...

    Parameters:
        file_path (str): Path to the raw CSV file.
        output_dir (str): Directory where the processed file will be saved.
    """
    keep_columns = [
        "abstract",
        "title",
        "publication_year",
        "index_terms.author_terms.terms",
        "index_terms.ieee_terms.terms",
    ]
    df = import_csv(file_path, keep_columns)

    # Combine fields into a single text input for the classifier
    def create_text_input(row):
        abstract = row["abstract"] if not pd.isna(row["abstract"]) else ""
        title = row["title"] if not pd.isna(row["title"]) else ""
        author_terms = (
            ", ".join(eval(row["index_terms.author_terms.terms"]))
            if not pd.isna(row["index_terms.author_terms.terms"])
            else ""
        )
        ieee_terms = (
            ", ".join(eval(row["index_terms.ieee_terms.terms"]))
            if not pd.isna(row["index_terms.ieee_terms.terms"])
            else ""
        )

        text_input = f"Title: {title}. Abstract: {abstract}. Keywords: {author_terms}, {ieee_terms}."
        return text_input

    # Apply preprocessing
    df["text_input"] = df.apply(create_text_input, axis=1)

    # Keep only the final fields
    processed_df = df[["text_input", "publication_year"]]

    # Save the processed CSV
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(file_path))
    processed_df.to_csv(output_file, index=False)
    print(f"Processed file saved to: {output_file}")


if __name__ == "__main__":
    """
    If this file is specifically executed, it should be directed to a specific
    `csv` file. To select it, argparse is used.
    """

    import argparse as ag

    parser = ag.ArgumentParser(description="Preprocess IEEE CSV files.")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,  # Ensure this argument is mandatory
        help="The name of the raw CSV file to preprocess (e.g. <theme>_<timestamp>.csv)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise FileNotFoundError(f"File '{args.file}' does not exist.")

    preprocess_csv(
        file_path=args.file,
        output_dir=os.path.join(config.ROOT_DIR, config.DATA_PROCESSED_DIR),
    )
