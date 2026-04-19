# Testing Runbook

This runbook covers all manual and automated verification steps for the IEEE Papers Mapper.

## Automated Tests

Run the full test suite:

```bash
make test
```

Run with verbose output for debugging:

```bash
make test-verbose
```

Run a specific test file:

```bash
.venv/bin/python -m pytest tests/test_pipeline.py -v
```

## Linting

Check formatting without changing files:

```bash
make lint
```

Auto-format:

```bash
make format
```

## Preflight Check

Run lint + tests together (the CI gate):

```bash
make check
```

## Manual Smoke Tests

### 1. API Fetch

Verify the IEEE API key works and papers can be fetched:

```bash
.venv/bin/python -c "
from ieee_papers_mapper.data.get_papers import get_papers
import ieee_papers_mapper.config.config as cfg

df = get_papers(
    query='machine learning',
    api_key=cfg.IEEE_API_KEY,
    start_year=cfg.IEEE_API_START_YEAR,
    start_record=1,
    max_records=3,
)
print(f'Fetched {len(df)} papers')
print(df[['title']].to_string())
"
```

Expected: 3 rows with paper titles. If the API key is missing or invalid, you'll see an `IEEEApiError`.

### 2. Processing Pipeline (Fetch + Validate)

Verify that raw API data is correctly parsed into Pydantic models:

```bash
.venv/bin/python -c "
from ieee_papers_mapper.data.get_papers import get_papers
from ieee_papers_mapper.data.process_papers import process_papers
import ieee_papers_mapper.config.config as cfg

df = get_papers(
    query='robotics', api_key=cfg.IEEE_API_KEY,
    start_year=cfg.IEEE_API_START_YEAR, start_record=1, max_records=3,
)
papers = process_papers(df)
for p in papers:
    print(f'{p.is_number}: {p.title[:60]}')
    print(f'  authors: {[a.full_name for a in p.authors][:3]}')
    print(f'  ieee_terms: {p.index_terms_ieee[:3]}')
"
```

Expected: 3 papers with populated authors and index terms. If any field fails validation, a `PaperValidationError` is raised immediately.

### 3. Dashboard

Verify the Dash web app boots and serves:

```bash
make dash-smoke
```

Or manually:

```bash
ieee-papers dashboard
# Open http://localhost:8050 in a browser
```

Expected: HTTP 200. The bar chart will be empty until the pipeline has populated the database.

### 4. Database Reset

Delete and recreate the database from scratch:

```bash
ieee-papers db-reset
```

Or via Make:

```bash
make db-reset
```

Expected: A fresh `ieee_papers.duckdb` is created with all 5 tables (papers, authors, index_terms, prompts, classification).

### 5. Full Pipeline (End-to-End)

Run the complete pipeline against the live API. This fetches papers, processes them into validated models, stores them in DuckDB, and classifies them with the transformer model.

**Warning:** The first run downloads the DeBERTa model (~700MB). Classification takes ~1-2s per paper.

```bash
ieee-papers run
```

Then verify the database contents:

```bash
ieee-papers verify
```

Expected: Non-zero counts across all 5 tables. Classification confidence scores should be between 0.0 and 1.0.

### 6. Lazy Classifier Import

Verify the transformer model is NOT loaded at import time:

```bash
time .venv/bin/python -c "from ieee_papers_mapper.data.classify_papers import classify_text"
```

Expected: Completes in under 1 second. If it takes 10+ seconds, the lazy-load is broken and the model is being loaded at import time.

## Docker

Build the image:

```bash
make docker-build
```

Start services (dashboard + pipeline):

```bash
make docker-up
```

Check logs:

```bash
make docker-logs
```

Verify the dashboard is accessible at `http://localhost:8050`.

Stop services:

```bash
make docker-down
```
