# API Reference

## Models (`models.py`)

### `Author`
Pydantic model for paper author metadata: `author_id`, `full_name`, `affiliation`.

### `ProcessedPaper`
Validated paper record at the processing boundary. Includes field constraints (non-negative counts, ISO 8601 date format, non-empty title).

### `ClassifiedPaper`
Classification result: `paper_id`, `category`, `confidence` (clamped to 0.0-1.0).

---

## Exceptions (`exceptions.py`)

### `IEEEApiError`
Raised when an IEEE API request fails (network error, HTTP error, rate limit).

### `PaperValidationError`
Raised when paper data fails Pydantic validation during processing.

---

## Data Layer

### `get_papers(query, start_year, api_key, max_records, start_record) -> pd.DataFrame`
Fetches papers from the IEEE Xplore API. Returns an empty DataFrame when no results are found. Raises `IEEEApiError` on failure.

### `process_papers(df_raw) -> list[ProcessedPaper]`
Transforms a raw API DataFrame into validated Pydantic models. Parses dates, index terms, and author metadata. Raises `PaperValidationError` on malformed data.

### `classify_text(text, timer) -> list[tuple[str, float]]`
Classifies a single text against configured categories using zero-shot DeBERTa. Classifier is lazy-loaded on first call.

### `classify_all_papers(df, timer) -> list[ClassifiedPaper]`
Classifies all papers in a DataFrame and returns validated `ClassifiedPaper` models.

---

## Repository (`repository.py`)

### `PaperRepository(connection)`
CRUD operations on the DuckDB database, accepting Pydantic models.

- `paper_exists(is_number) -> bool`
- `insert_paper(paper: ProcessedPaper) -> int`
- `insert_full_paper(paper: ProcessedPaper) -> None` — inserts paper, authors, terms, and prompt; skips duplicates
- `get_unclassified_papers() -> pd.DataFrame`
- `insert_classifications(classifications: list[ClassifiedPaper]) -> None`

---

## Database (`database.py`)

### `Database(name, filepath)`
Connection lifecycle and schema management (DDL). Creates tables with foreign key ordering on first run.

- `initialise()` — creates missing tables
- `connect() / close()` — connection lifecycle

---

## Pipeline (`pipeline.py`)

### `run_pipeline() -> bool`
Orchestrates the full pipeline: fetch, process, store, classify. Returns `True` if new papers were processed.

### `ProgressTracker(filename, config_dir)`
Tracks per-category pagination state in a JSON file for incremental fetching.
