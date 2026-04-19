# Usage Guide

## Running the Pipeline

Fetch, process, classify, and store papers on a schedule:

```bash
python -m ieee_papers_mapper.main --hours 24
```

This runs the pipeline immediately, then repeats every 24 hours. Adjust the interval with `--weeks`, `--days`, `--hours`, `--minutes`, or `--seconds`.

For a one-shot run (no scheduler):

```bash
python -c "from ieee_papers_mapper.data.pipeline import run_pipeline; run_pipeline()"
```

## Running the Dashboard

```bash
python -m ieee_papers_mapper.app.dash_webapp
```

Open `http://localhost:8050` to see a bar chart of paper counts by category. The chart auto-refreshes every 10 seconds.

## Database Management

Reset the database (deletes all data):

```bash
make db-reset
```

Inspect the database directly:

```bash
python -c "
import duckdb, ieee_papers_mapper.config.config as cfg
conn = duckdb.connect(cfg.DB_PATH, read_only=True)
for table in ['papers', 'authors', 'index_terms', 'prompts', 'classification']:
    count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    print(f'{table}: {count} rows')
conn.close()
"
```

## Configuration

All settings are in `src/ieee_papers_mapper/config/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `IEEE_API_KEY` | from `.env` | IEEE Xplore API key |
| `IEEE_API_START_YEAR` | 2024 | Earliest publication year to fetch |
| `IEEE_API_MAX_RECORDS` | 50 | Papers per API request (max 200) |
| `CATEGORIES` | machine learning, power electronics, robotics | Search queries |
| `DEBERTA_V3_MODEL_NAME` | MoritzLaurer/deberta-v3-large-zeroshot-v2.0 | Classifier model |
