#!/usr/bin/env python3

"""

"""


import os
import pandas as pd
import config
import ast
from typing import List


def process_papers(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess a single CSV file to retain relevant information for classification.
    """
    keep_columns = [
        "is_number",
        "insert_date",
        "publication_year",
        "download_count",
        "citing_patent_count",
        "title",
        "abstract",
        "index_terms.author_terms.terms",
        "index_terms.ieee_terms.terms",
        "index_terms.dynamic_index_terms.terms",
        "authors.authors",
    ]

    df_processed = df_raw[keep_columns].copy()

    # Transform date columns
    df_processed["insert_date"] = pd.to_datetime(
        df_processed["insert_date"]
    ).dt.strftime("%Y%m%d")
    df_processed["publication_year"] = df_processed["publication_year"].astype(str)

    # Transform index_terms columns
    for col in [
        "index_terms.author_terms.terms",
        "index_terms.ieee_terms.terms",
        "index_terms.dynamic_index_terms.terms",
    ]:
        df_processed[col] = df_processed[col].apply(eval)

    # Rename index_terms columns
    df_processed.rename(
        columns={
            "index_terms.author_terms.terms": "index_terms_author",
            "index_terms.ieee_terms.terms": "index_terms_ieee",
            "index_terms.dynamic_index_terms.terms": "index_terms_dynamic",
        },
        inplace=True,
    )

    # Extract author information
    def _extract_author_info(authors_str):
        authors = ast.literal_eval(authors_str)
        return [
            {
                # Only keeping the "order=1" author
                'author_id': author['id'],
                'author_full_name': author['full_name'],
                'author_affiliation': author['affiliation'],
                # 'author_url': author['authorUrl'],
                # 'author_order': author['author_order'],
                # 'author_affiliations': author['authorAffiliations']['authorAffiliation']
            }
            for author in authors
        ]

    df_processed['authors'] = df_processed['authors.authors'].apply(_extract_author_info)
    df_processed.drop('authors.authors', axis=1, inplace=True)

    # Create prompt column
    # prompt: title - abstract - index_terms
    def _create_prompt(row):
        title = row['title']
        abstract = row['abstract']
        all_terms = row['index_terms_author'] + row['index_terms_ieee'] + row['index_terms_dynamic']
        index_terms = ', '.join(all_terms)
        return f"title: {title} - abstract: {abstract} - index_terms: {index_terms}"
    df_processed["prompt"] = df_processed.apply(_create_prompt, axis=1)

    # Reorder columns
    column_order = [
        "is_number",
        "insert_date",
        "publication_year",
        "download_count",
        "citing_patent_count",
        "index_terms_author",
        "index_terms_ieee",
        "index_terms_dynamic",
        "authors",
        "title",
        "abstract",
        "prompt",
    ]
    df_processed = df_processed[column_order]

    return df_processed


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
        required=True,
        help="The path to the raw CSV file to preprocess",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=os.path.join(config.ROOT_DIR, config.DATA_PROCESSED_DIR),
        help="The directory to save the processed CSV file",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise FileNotFoundError(f"File '{args.file}' does not exist.")

    # Read the input CSV file
    df_raw = pd.read_csv(args.file)

    # Process the papers
    df_processed = process_papers(df_raw)

    # Create the output filename
    input_filename = os.path.basename(args.file)
    output_filename = f"processed_{input_filename}"
    output_path = os.path.join(args.output, output_filename)

    # Ensure the output directory exists
    os.makedirs(args.output, exist_ok=True)

    # Save the processed DataFrame to a CSV file
    df_processed.to_csv(output_path, index=False)

    print(f"Processed file saved to: {output_path}")
