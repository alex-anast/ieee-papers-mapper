# API Reference

## Models (`models.py`)

### `Author`

Pydantic model representing a paper author.

```python
class Author(BaseModel):
    author_id: str
    full_name: str
    affiliation: str
```

Used during processing to validate and structure author metadata extracted from the IEEE API response. Each `ProcessedPaper` contains a list of `Author` instances.

---

### `ProcessedPaper`

Validated paper record created at the processing boundary. Enforces data contracts before storage.

```python
class ProcessedPaper(BaseModel):
    is_number: str                              # IEEE article identifier
    insert_date: str                            # ISO 8601 date (YYYY-MM-DD), validated by field_validator
    publication_year: str
    download_count: int = Field(ge=0)           # Non-negative
    citing_patent_count: int = Field(ge=0)      # Non-negative
    title: str = Field(min_length=1)            # Must not be empty
    abstract: str
    index_terms_ieee: list[str] = []
    index_terms_dynamic: list[str] = []
    authors: list[Author]
    prompt: str                                 # Constructed from title + abstract + terms
```

The `insert_date` field has a custom validator that checks the date can be parsed as `%Y-%m-%d`. Created by `process_papers()` and consumed by `PaperRepository.insert_full_paper()`.

---

### `ClassifiedPaper`

Classification result for a single paper-category pair.

```python
class ClassifiedPaper(BaseModel):
    paper_id: int                               # Foreign key to papers table
    category: str                               # Classification label
    confidence: float = Field(ge=0.0, le=1.0)   # Score clamped to [0.0, 1.0]
```

Created by `classify_all_papers()` and consumed by `PaperRepository.insert_classifications()`.

---

## Exceptions (`exceptions.py`)

### `IEEEPapersError`

Base exception for the project. All custom exceptions inherit from this.

```python
class IEEEPapersError(Exception): ...
```

---

### `IEEEApiError`

Raised when an IEEE API request fails (network error, HTTP error, rate limit). Caught per-category in the pipeline so that one failing query does not abort the entire run.

```python
class IEEEApiError(IEEEPapersError): ...
```

Raised by: `get_papers()`

---

### `PaperValidationError`

Raised when paper data fails Pydantic validation during processing. Always fatal for the affected record.

```python
class PaperValidationError(IEEEPapersError): ...
```

Raised by: `process_papers()`, `_parse_date()`

---

## CLI (`cli.py`)

Click-based command group installed as the `ieee-papers` console script.

### `cli` (group)

```python
@click.group()
def cli(): ...
```

Top-level group. All commands below are subcommands of this group.

---

### `run`

```python
@cli.command()
@click.option("--weeks", default=0)
@click.option("--days", default=0)
@click.option("--hours", default=0)
@click.option("--minutes", default=0)
@click.option("--seconds", default=0)
def run(weeks, days, hours, minutes, seconds): ...
```

Runs the pipeline. If no interval flags are provided (or all are zero), executes a single pipeline run and exits. If any interval flag is non-zero, creates a `Scheduler` that runs the pipeline immediately and repeats at the configured interval.

---

### `dashboard`

```python
@cli.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8050)
@click.option("--debug/--no-debug", default=True)
def dashboard(host, port, debug): ...
```

Launches the Plotly Dash web application on the specified host and port.

---

### `verify`

```python
@cli.command()
def verify(): ...
```

Prints system health information: API key status, database path and table row counts, and whether the classifier module is importable. Does not load the transformer model.

---

### `db-reset`

```python
@cli.command("db-reset")
@click.confirmation_option(prompt="This will delete all data. Continue?")
def db_reset(): ...
```

Deletes the DuckDB file (and its WAL file if present), then creates a fresh database with all tables. Requires confirmation unless `--yes` is passed.

---

## Data Layer

### `get_papers()`

```python
def get_papers(
    query: str,
    start_year: str,
    api_key: str,
    max_records: int,
    start_record: int,
) -> pd.DataFrame
```

Fetches papers from the IEEE Xplore API for the given query. Sends a GET request to the IEEE search endpoint with parameterized query options (content type: Journals, sorted by article number ascending).

**Returns:** `pd.DataFrame` -- Normalized JSON response. Empty DataFrame if no results.

**Raises:** `IEEEApiError` -- On any `requests.exceptions.RequestException`.

---

### `process_papers()`

```python
def process_papers(df_raw: pd.DataFrame) -> list[ProcessedPaper]
```

Transforms raw API DataFrame rows into validated Pydantic models. For each row:

1. Extracts author metadata from the nested `authors.authors` column into `Author` models.
2. Parses IEEE and dynamic index terms (handles both list and string representations).
3. Converts `insert_date` from `YYYYMMDD` to `YYYY-MM-DD`.
4. Constructs a classification prompt from title, abstract, and terms.

**Returns:** `list[ProcessedPaper]` -- One model per valid row.

**Raises:** `PaperValidationError` -- If any row fails Pydantic validation or has a missing required field.

---

### `classify_text()`

```python
def classify_text(text: str, timer: bool = False) -> list[tuple[str, float]]
```

Classifies a single text against all configured categories using multi-label zero-shot classification. The DeBERTa classifier is lazy-loaded on first call.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | The input text to classify (typically a paper prompt). |
| `timer` | `bool` | If `True`, logs classification time at DEBUG level. |

**Returns:** `list[tuple[str, float]]` -- List of `(category, confidence_score)` tuples.

---

### `classify_all_papers()`

```python
def classify_all_papers(df: pd.DataFrame, timer: bool = False) -> list[ClassifiedPaper]
```

Classifies all papers in a DataFrame and returns validated models.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `df` | `pd.DataFrame` | Must contain `paper_id` and `prompt_text` columns. |
| `timer` | `bool` | If `True`, logs per-paper and aggregate classification times. |

**Returns:** `list[ClassifiedPaper]` -- One `ClassifiedPaper` per paper-category pair.

---

## Database (`database.py`)

### `Database`

```python
class Database:
    def __init__(self, name: str, filepath: Optional[str] = None): ...
```

Connection lifecycle and schema manager for the DuckDB database. Creates the database file at `{filepath}/{name}.duckdb` (or `{name}.duckdb` in the current directory if `filepath` is `None`).

**Methods:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `initialise()` | `None` | Creates missing tables. Creates all tables from scratch if the DB file does not exist. |
| `create_all_tables()` | `None` | Creates all five tables in foreign-key order. |
| `create_tables(tables, cursor=None)` | `None` | Creates a specific subset of tables. |
| `connect()` | `bool` | Opens a connection if not already connected. Returns `True` on success. |
| `close()` | `None` | Closes the active connection. |
| `get_existing_tables()` | `list[str]` | Queries `information_schema.tables` for existing table names. |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `file_exists` | `bool` | Whether the database file exists on disk. |
| `is_connected` | `bool` | Whether the connection is currently open. |

**Schema (5 tables):**

- `papers` -- Core paper metadata (PK: `paper_id`, auto-incremented via sequence).
- `authors` -- Author records, FK to `papers`.
- `index_terms` -- IEEE and dynamic index terms, FK to `papers`.
- `prompts` -- Classification prompt text, FK to `papers`.
- `classification` -- Classification results (category + confidence), FK to `papers`.

---

## Repository (`repository.py`)

### `PaperRepository`

```python
class PaperRepository:
    def __init__(self, connection: duckdb.DuckDBPyConnection): ...
```

Typed CRUD operations on the DuckDB database. Accepts and returns Pydantic models; executes parameterized SQL internally.

**Methods:**

| Method | Parameters | Return Type | Description |
|--------|-----------|-------------|-------------|
| `paper_exists()` | `is_number: str` | `bool` | Checks if a paper with the given IEEE number exists. |
| `insert_paper()` | `paper: ProcessedPaper` | `int` | Inserts core paper metadata. Returns the generated `paper_id`. |
| `insert_authors()` | `paper_id: int, authors: list[Author]` | `None` | Inserts author records linked to a paper. |
| `insert_index_terms()` | `paper_id: int, term_type: str, terms: list[str]` | `None` | Inserts index terms (IEEE or dynamic) linked to a paper. |
| `insert_prompt()` | `paper_id: int, prompt: str` | `None` | Inserts the classification prompt linked to a paper. |
| `insert_full_paper()` | `paper: ProcessedPaper` | `None` | Inserts a paper across all tables. Skips if the paper already exists (deduplication on `is_number`). |
| `get_unclassified_papers()` | -- | `pd.DataFrame` | Returns papers that have no classification rows. DataFrame has columns `paper_id` and `prompt_text`. |
| `insert_classifications()` | `classifications: list[ClassifiedPaper]` | `None` | Bulk-inserts classification results via a registered DataFrame view. |

---

## Pipeline (`pipeline.py`)

### `run_pipeline()`

```python
def run_pipeline() -> bool
```

Orchestrates the full pipeline:

1. Initialises the database (creates tables if needed).
2. Fetches papers for each configured category with incremental pagination.
3. Stores validated papers via the repository.
4. Classifies any unclassified papers.
5. Closes the database connection.

**Returns:** `bool` -- `True` if new papers were fetched and stored, `False` otherwise.

---

### `ProgressTracker`

```python
class ProgressTracker:
    def __init__(self, filename: str, config_dir: str): ...
```

Tracks per-category pagination state in a JSON file for incremental fetching. The JSON file maps category names to their last-fetched `start_record`.

**Methods:**

| Method | Parameters | Return Type | Description |
|--------|-----------|-------------|-------------|
| `load()` | -- | `dict[str, int]` | Loads progress from the JSON file. Returns empty dict if the file does not exist. |
| `save()` | `progress: dict[str, int]` | `None` | Writes the current progress to the JSON file. |

**Example JSON file (`progress.json`):**

```json
{
    "machine learning": 151,
    "power electronics": 51,
    "robotics": 101
}
```

---

## Scheduler (`config/scheduler.py`)

### `Scheduler`

```python
class Scheduler:
    def __init__(self, job: Callable, **interval_kwargs): ...
```

Wraps APScheduler's `BackgroundScheduler` to execute a callable at specified intervals. Accepts any callable via dependency injection.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `job` | `Callable` | The function to execute on each trigger. |
| `**interval_kwargs` | `dict` | Interval keyword arguments: `weeks`, `days`, `hours`, `minutes`, `seconds`. If all values are zero or none are provided, defaults to weekly. |

**Methods:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `start()` | `None` | Adds the job to the scheduler, starts it, then runs the job immediately. |
| `stop()` | `None` | Shuts down the scheduler gracefully. |

---

## Dashboard (`app/dash_webapp.py`)

### `fetch_data()`

```python
def fetch_data(threshold: float = 0.5) -> pd.DataFrame
```

Queries DuckDB for paper counts grouped by category, filtered by a minimum confidence threshold. Opens a read-only connection, executes a parameterized query, and returns the result.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `threshold` | `float` | `0.5` | Minimum classification confidence to include a paper. |

**Returns:** `pd.DataFrame` -- Columns: `category`, `paper_count`.

---

### `update_graph()`

```python
@app.callback(Output("papers-bar-chart", "figure"), [Input("interval-component", "n_intervals")])
def update_graph(n_intervals: int) -> go.Figure
```

Dash callback that fires every 10 seconds (driven by `dcc.Interval`). Calls `fetch_data()` and renders a Plotly bar chart of paper counts by category.

**Returns:** `go.Figure` -- Updated bar chart with transition animation.

---

## Logging (`config/logging_config.py`)

### `setup_logging()`

```python
def setup_logging(level: int = logging.DEBUG) -> logging.Logger
```

Configures and returns the shared `ieee_logger` with structured JSON output via `python-json-logger`. Log entries include fields: `timestamp`, `level`, `name`, `module`, `function`, `message`.

Idempotent: if handlers are already attached, returns the existing logger without adding duplicates.
