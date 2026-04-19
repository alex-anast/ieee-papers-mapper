"""
Dashboard Queries
=================

Centralised read-only SQL for every dashboard visualisation.
All functions accept filter parameters and return pandas DataFrames.
A module-level DuckDB connection is opened once in read-only mode.
"""

import os
import duckdb
import pandas as pd
from ieee_papers_mapper.config import config as cfg

_conn: duckdb.DuckDBPyConnection | None = None


def _get_conn() -> duckdb.DuckDBPyConnection:
    global _conn
    if _conn is None and os.path.exists(cfg.DB_PATH):
        _conn = duckdb.connect(cfg.DB_PATH, read_only=True)
    if _conn is None:
        raise RuntimeError(f"Database not found at {cfg.DB_PATH}")
    return _conn


def _where_clause(
    confidence: float = 0.5,
    categories: list[str] | None = None,
    year_range: list[int] | None = None,
) -> tuple[str, list]:
    """Build a reusable WHERE fragment and parameter list from filter values."""
    clauses = ["c.confidence >= ?"]
    params: list = [confidence]

    if categories:
        placeholders = ", ".join("?" for _ in categories)
        clauses.append(f"c.category IN ({placeholders})")
        params.extend(categories)

    if year_range and len(year_range) == 2:
        clauses.append("p.publication_year BETWEEN ? AND ?")
        params.extend(year_range)

    return " AND ".join(clauses), params


# -- Overview KPIs -----------------------------------------------------------

def kpi_totals() -> dict:
    """Return scalar KPIs for the overview cards."""
    row = _get_conn().execute("""
        SELECT
            (SELECT COUNT(*) FROM papers) AS total_papers,
            (SELECT COUNT(DISTINCT name) FROM authors) AS total_authors,
            (SELECT ROUND(AVG(confidence), 2) FROM classification) AS avg_confidence,
            (SELECT COUNT(DISTINCT affiliation) FROM authors) AS total_affiliations
    """).fetchone()
    return {
        "total_papers": row[0],
        "total_authors": row[1],
        "avg_confidence": row[2],
        "total_affiliations": row[3],
    }


# -- Category bar chart ------------------------------------------------------

def papers_by_category(
    confidence: float = 0.5,
    categories: list[str] | None = None,
    year_range: list[int] | None = None,
) -> pd.DataFrame:
    where, params = _where_clause(confidence, categories, year_range)
    return _get_conn().execute(f"""
        SELECT c.category, COUNT(*) AS paper_count
        FROM classification c
        JOIN papers p ON c.paper_id = p.paper_id
        WHERE {where}
        GROUP BY c.category
        ORDER BY paper_count DESC
    """, params).fetchdf()


# -- Confidence distribution -------------------------------------------------

def confidence_distribution(
    categories: list[str] | None = None,
    year_range: list[int] | None = None,
) -> pd.DataFrame:
    clauses = []
    params: list = []

    if categories:
        placeholders = ", ".join("?" for _ in categories)
        clauses.append(f"c.category IN ({placeholders})")
        params.extend(categories)
    if year_range and len(year_range) == 2:
        clauses.append("p.publication_year BETWEEN ? AND ?")
        params.extend(year_range)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""

    return _get_conn().execute(f"""
        SELECT c.category, c.confidence
        FROM classification c
        JOIN papers p ON c.paper_id = p.paper_id
        {where}
    """, params).fetchdf()


# -- Papers table ------------------------------------------------------------

def papers_table(
    confidence: float = 0.5,
    categories: list[str] | None = None,
    year_range: list[int] | None = None,
) -> pd.DataFrame:
    where, params = _where_clause(confidence, categories, year_range)
    return _get_conn().execute(f"""
        SELECT
            p.paper_id,
            p.title,
            c.category,
            ROUND(c.confidence, 3) AS confidence,
            p.publication_year,
            p.download_count,
            p.citing_patent_count,
            STRING_AGG(DISTINCT a.name, ', ') AS authors
        FROM papers p
        JOIN classification c ON c.paper_id = p.paper_id
        LEFT JOIN authors a ON a.paper_id = p.paper_id
        WHERE {where}
        GROUP BY p.paper_id, p.title, c.category, c.confidence,
                 p.publication_year, p.download_count, p.citing_patent_count
        ORDER BY c.confidence DESC
    """, params).fetchdf()


def paper_detail(paper_id: int) -> dict:
    """Full detail for a single paper (abstract, terms, authors)."""
    conn = _get_conn()
    paper = conn.execute("""
        SELECT p.title, p.abstract, c.category, ROUND(c.confidence, 3) AS confidence,
               p.publication_year, p.download_count, p.citing_patent_count
        FROM papers p
        JOIN classification c ON c.paper_id = p.paper_id
        WHERE p.paper_id = ?
    """, [paper_id]).fetchone()

    if paper is None:
        return {}

    authors = conn.execute("""
        SELECT name, affiliation FROM authors WHERE paper_id = ?
    """, [paper_id]).fetchdf()

    terms = conn.execute("""
        SELECT term_type, term FROM index_terms WHERE paper_id = ?
    """, [paper_id]).fetchdf()

    return {
        "title": paper[0],
        "abstract": paper[1],
        "category": paper[2],
        "confidence": paper[3],
        "publication_year": paper[4],
        "download_count": paper[5],
        "citing_patent_count": paper[6],
        "authors": authors.to_dict("records"),
        "terms": terms.to_dict("records"),
    }


# -- Trends ------------------------------------------------------------------

def papers_over_time(
    confidence: float = 0.5,
    categories: list[str] | None = None,
    year_range: list[int] | None = None,
) -> pd.DataFrame:
    where, params = _where_clause(confidence, categories, year_range)
    return _get_conn().execute(f"""
        SELECT
            DATE_TRUNC('month', p.insert_date) AS month,
            c.category,
            COUNT(*) AS paper_count
        FROM papers p
        JOIN classification c ON c.paper_id = p.paper_id
        WHERE {where}
        GROUP BY month, c.category
        ORDER BY month
    """, params).fetchdf()


def downloads_vs_citations(
    confidence: float = 0.5,
    categories: list[str] | None = None,
    year_range: list[int] | None = None,
) -> pd.DataFrame:
    where, params = _where_clause(confidence, categories, year_range)
    return _get_conn().execute(f"""
        SELECT
            p.title,
            p.download_count,
            p.citing_patent_count,
            c.category,
            ROUND(c.confidence, 3) AS confidence
        FROM papers p
        JOIN classification c ON c.paper_id = p.paper_id
        WHERE {where}
    """, params).fetchdf()


# -- Terms -------------------------------------------------------------------

def top_terms(
    n: int = 15,
    term_type: str | None = None,
    confidence: float = 0.5,
    categories: list[str] | None = None,
    year_range: list[int] | None = None,
) -> pd.DataFrame:
    where, params = _where_clause(confidence, categories, year_range)

    if term_type:
        where += " AND it.term_type = ?"
        params.append(term_type)

    params.append(n)

    return _get_conn().execute(f"""
        SELECT it.term, it.term_type, COUNT(*) AS freq
        FROM index_terms it
        JOIN papers p ON it.paper_id = p.paper_id
        JOIN classification c ON c.paper_id = p.paper_id
        WHERE {where}
        GROUP BY it.term, it.term_type
        ORDER BY freq DESC
        LIMIT ?
    """, params).fetchdf()


# -- Filter metadata ---------------------------------------------------------

def available_years() -> list[int]:
    rows = _get_conn().execute(
        "SELECT DISTINCT publication_year FROM papers ORDER BY publication_year"
    ).fetchall()
    return [r[0] for r in rows]


def available_categories() -> list[str]:
    rows = _get_conn().execute(
        "SELECT DISTINCT category FROM classification ORDER BY category"
    ).fetchall()
    return [r[0] for r in rows]
