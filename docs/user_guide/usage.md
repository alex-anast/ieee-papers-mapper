# Usage Guide

## CLI Overview

The `ieee-papers` command is installed as a console script via `pyproject.toml`. All operations go through it.

```
Usage: ieee-papers [OPTIONS] COMMAND [ARGS]...

  IEEE Papers Mapper -- fetch, classify, and visualize IEEE research papers.

Options:
  --help  Show this message and exit.

Commands:
  dashboard  Launch the Dash dashboard.
  db-reset   Delete and recreate the database from scratch.
  run        Run the pipeline. One-shot by default, add interval flags to schedule.
  verify     Check system health: API key, database, model availability.
```

---

## Running the Pipeline

### One-Shot Mode

Fetch papers, process, store in DuckDB, classify, then exit:

```bash
ieee-papers run
```

### Scheduled Mode

Run immediately, then repeat at the given interval:

```bash
ieee-papers run --hours 24
```

Interval flags can be combined. All flags default to 0; if none are provided, the pipeline runs once and exits. If all provided values are zero, the scheduler defaults to a weekly interval.

| Flag | Description |
|------|-------------|
| `--weeks N` | Repeat every N weeks |
| `--days N` | Repeat every N days |
| `--hours N` | Repeat every N hours |
| `--minutes N` | Repeat every N minutes |
| `--seconds N` | Repeat every N seconds |

Press `Ctrl+C` to stop the scheduler gracefully.

---

## Launching the Dashboard

```bash
ieee-papers dashboard
```

Open `http://localhost:8050` to see a bar chart of paper counts by category. The chart auto-refreshes every 10 seconds to reflect the latest classification data.

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `0.0.0.0` | Host to bind to |
| `--port` | `8050` | Port to serve on |
| `--debug/--no-debug` | `--debug` | Enable or disable Dash debug mode |

---

## System Health Check

```bash
ieee-papers verify
```

Displays:

- Whether the IEEE API key is configured
- Database location and row counts for all five tables
- Whether the classifier module is importable (without loading the model)

---

## Database Management

### Reset the Database

Delete all data and recreate the schema from scratch:

```bash
ieee-papers db-reset
```

You will be prompted for confirmation. To skip the prompt (useful in scripts):

```bash
ieee-papers db-reset --yes
```

Or via Make:

```bash
make db-reset
```

---

## Example Workflow: First Run

A complete walkthrough from a clean clone to a populated dashboard:

```bash
# 1. Clone and install
git clone https://github.com/alex-anast/ieee-papers-mapper.git
cd ieee-papers-mapper
cp .env.example .env
# Edit .env and add your IEEE_API_KEY
make install

# 2. Verify the setup
ieee-papers verify

# 3. Initialize the database
ieee-papers db-reset --yes

# 4. Run the pipeline (fetches papers, classifies them)
ieee-papers run

# 5. Launch the dashboard
ieee-papers dashboard
# Open http://localhost:8050 in a browser
```

The first `ieee-papers run` will download the DeBERTa model (~700 MB) before classification begins. Subsequent runs use the cached model.

---

## Docker Usage

Docker Compose runs two services: `dashboard` (the Dash web app) and `pipeline` (runs the fetch/classify pipeline every 24 hours).

### Build and Start

```bash
cp .env.example .env          # add your IEEE_API_KEY
make docker-build
make docker-up
```

### View Logs

```bash
make docker-logs
```

### Stop Services

```bash
make docker-down
```

The dashboard is available at `http://localhost:8050`. Both services share a named volume (`app-data`) for the DuckDB database and a second volume (`huggingface-cache`) for the transformer model cache.

The pipeline service depends on the dashboard service being healthy (HTTP 200 on port 8050) before starting, ensuring the database is accessible before the pipeline writes to it.

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `IEEE_API_KEY` | Yes | -- | Your IEEE Xplore API key. Obtain one at [developer.ieee.org](https://developer.ieee.org/). |
| `DATA_DIR` | No | `src/ieee_papers_mapper/` | Override the directory for the DuckDB database and progress tracker. Used by Docker Compose to point both services at a shared volume. |

Both variables can be set in a `.env` file at the project root (loaded automatically via `python-dotenv`).

---

## Configuration

Application-level settings are defined in `src/ieee_papers_mapper/config/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `IEEE_API_START_YEAR` | `2024` | Earliest publication year to fetch |
| `IEEE_API_MAX_RECORDS` | `50` | Papers per API request (IEEE max is 200) |
| `CATEGORIES` | `["machine learning", "power electronics", "robotics"]` | Search queries sent to the IEEE API |
| `DEBERTA_V3_MODEL_NAME` | `MoritzLaurer/deberta-v3-large-zeroshot-v2.0` | Hugging Face model identifier for zero-shot classification |
| `DB_TABLES` | `["papers", "authors", "index_terms", "prompts", "classification"]` | Expected database tables (created on init) |

To change these, edit `config.py` directly. There is no external configuration file beyond `.env` for the API key and data directory.
