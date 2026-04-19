# Installation Guide

## Prerequisites

- Python 3.12 or later
- Git
- An [IEEE Xplore API key](https://developer.ieee.org/)

## Quick Start (Makefile)

```bash
git clone https://github.com/alex-anast/ieee-papers-mapper.git
cd ieee-papers-mapper
cp .env.example .env        # add your IEEE_API_KEY
make install                # creates venv and installs everything
make check                  # lint + tests
```

## Manual Installation

1. Clone the repository:

```bash
git clone https://github.com/alex-anast/ieee-papers-mapper.git
cd ieee-papers-mapper
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies (CPU-only PyTorch):

```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
pip install -e .
```

4. Configure the API key:

```bash
cp .env.example .env
# Edit .env and set IEEE_API_KEY=your_key_here
```

## Docker

Build and start both services (dashboard + pipeline):

```bash
cp .env.example .env        # add your IEEE_API_KEY
make docker-build
make docker-up
```

The dashboard will be available at `http://localhost:8050`. The pipeline service runs every 24 hours in the background.

Docker Compose uses two named volumes:

| Volume | Purpose |
|--------|---------|
| `app-data` | Shared DuckDB database and progress tracker between services |
| `huggingface-cache` | Persists the downloaded DeBERTa model across container restarts |

## Verify Installation

After installation, run the built-in health check to confirm everything is working:

```bash
ieee-papers verify
```

Expected output:

```
=== IEEE Papers Mapper -- System Verify ===

API key:    set (your...)
Database:   NOT FOUND at /path/to/ieee_papers.duckdb
  Run: ieee-papers db-reset

Classifier: available (lazy-load, not yet loaded)
```

If the database does not exist yet, create it:

```bash
ieee-papers db-reset --yes
```

Then re-run `ieee-papers verify` to confirm all five tables are present (papers, authors, index_terms, prompts, classification).

## Note on the DeBERTa Model

The zero-shot classifier uses the `MoritzLaurer/deberta-v3-large-zeroshot-v2.0` model from Hugging Face. This model is approximately **700 MB** and is downloaded automatically on the first classification run, not at install time.

The download happens lazily when `classify_text()` is first called. Subsequent runs use the cached model from `~/.cache/huggingface/`. If you are behind a firewall or on a restricted network, you may need to download the model in advance or configure a Hugging Face mirror.
