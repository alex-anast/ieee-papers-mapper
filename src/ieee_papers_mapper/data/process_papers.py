#!/usr/bin/env python3

import ast
import logging
import pandas as pd
from datetime import datetime
from pydantic import ValidationError
from ieee_papers_mapper.models import ProcessedPaper, Author
from ieee_papers_mapper.exceptions import PaperValidationError

logger = logging.getLogger("ieee_logger")


def process_papers(df_raw: pd.DataFrame) -> list[ProcessedPaper]:
    papers = []
    for _, row in df_raw.iterrows():
        try:
            authors = _extract_author_info(row.get("authors.authors", "[]"))
            ieee_terms = _safe_parse_list(row.get("index_terms.ieee_terms.terms", "[]"))
            dynamic_terms = _safe_parse_list(
                row.get("index_terms.dynamic_index_terms.terms", "[]")
            )
            insert_date = _parse_date(str(row["insert_date"]))

            paper = ProcessedPaper(
                is_number=str(row["is_number"]),
                insert_date=insert_date,
                publication_year=str(row["publication_year"]),
                download_count=int(row.get("download_count", 0)),
                citing_patent_count=int(row.get("citing_patent_count", 0)),
                title=row["title"],
                abstract=row["abstract"],
                index_terms_ieee=ieee_terms,
                index_terms_dynamic=dynamic_terms,
                authors=authors,
                prompt=_create_prompt(
                    row["title"], row["abstract"], ieee_terms, dynamic_terms
                ),
            )
            papers.append(paper)
        except (ValidationError, KeyError) as e:
            raise PaperValidationError(
                f"Failed to validate paper {row.get('is_number', 'unknown')}: {e}"
            ) from e
    return papers


def _parse_date(raw: str) -> str:
    try:
        return datetime.strptime(raw, "%Y%m%d").strftime("%Y-%m-%d")
    except ValueError as e:
        raise PaperValidationError(f"Invalid date format '{raw}': {e}") from e


def _safe_parse_list(value) -> list:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            logger.warning(f"Failed to parse list: {value}. Error: {e}")
            return []
    return []


def _extract_author_info(authors_raw) -> list[Author]:
    authors = _safe_parse_list(authors_raw)
    return [
        Author(
            author_id=str(author["id"]),
            full_name=author["full_name"],
            affiliation=author["affiliation"],
        )
        for author in authors
    ]


def _create_prompt(
    title: str, abstract: str, ieee_terms: list[str], dynamic_terms: list[str]
) -> str:
    all_terms = ieee_terms + dynamic_terms
    index_terms = ", ".join(all_terms)
    return f"title: {title} - abstract: {abstract} - index_terms: {index_terms}"
