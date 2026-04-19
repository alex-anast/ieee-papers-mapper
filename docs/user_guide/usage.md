# Usage Guide

## CLI

The `ieee-papers` command is installed as a console script. All operations go through it.

### Running the Pipeline

One-shot (fetch, process, classify, store, then exit):

```bash
ieee-papers run
```

Scheduled (runs immediately, then repeats on the interval):

```bash
ieee-papers run --hours 24
```

Adjust with `--weeks`, `--days`, `--hours`, `--minutes`, or `--seconds`.

### Running the Dashboard

```bash
ieee-papers dashboard
```

Open `http://localhost:8050` to see a bar chart of paper counts by category. The chart auto-refreshes every 10 seconds.

Options: `--host`, `--port`, `--debug/--no-debug`.

### System Health Check

```bash
ieee-papers verify
```

Shows API key status, database table counts, and classifier availability.

## Database Management

Reset the database (deletes all data):

```bash
ieee-papers db-reset
```

Or via Make:

```bash
make db-reset
```

Inspect the database directly:

```bash
ieee-papers verify
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
