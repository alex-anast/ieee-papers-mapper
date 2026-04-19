# IEEE Papers Mapper

Automated pipeline for fetching, classifying, and visualizing IEEE research papers using zero-shot NLP and a DuckDB analytical store.

![Tests](https://github.com/alex-anast/ieee-papers-mapper/actions/workflows/test.yml/badge.svg)
![License](https://img.shields.io/github/license/alex-anast/ieee-papers-mapper)
![Last Commit](https://img.shields.io/github/last-commit/alex-anast/ieee-papers-mapper)

---

## What This Project Does

- **Fetches** research papers from the IEEE Xplore API with incremental pagination that resumes across runs.
- **Validates** every record through Pydantic models, rejecting malformed data at the boundary rather than letting it propagate silently.
- **Classifies** papers into configurable categories using a DeBERTa-v3-large zero-shot transformer, loaded lazily to keep startup fast.
- **Visualizes** classified paper counts in a Plotly Dash dashboard that auto-refreshes every 10 seconds.
- **Monitors** pipeline health through Prometheus metrics, health endpoints, and a pre-built Grafana dashboard.

## Quick Start

```bash
git clone https://github.com/alex-anast/ieee-papers-mapper.git
cd ieee-papers-mapper
cp .env.example .env          # add your IEEE_API_KEY
make install                   # creates venv, installs deps + package
ieee-papers run                # fetch, classify, store
ieee-papers dashboard          # open http://localhost:8050
```

See the [Installation Guide](user_guide/installation.md) for detailed setup instructions.

## Documentation

| Section | Description |
|---------|-------------|
| [Overview](user_guide/overview.md) | Pipeline architecture, data flow, and design decisions |
| [Installation](user_guide/installation.md) | Prerequisites, setup (local and Docker), verification |
| [Usage](user_guide/usage.md) | CLI commands, configuration, environment variables |
| [Observability](user_guide/observability.md) | Metrics, health endpoints, Grafana dashboard, structured logging |
| [Code Structure](developer_guide/code_structure.md) | Module layout, design patterns, data flow trace |
| [Testing Runbook](developer_guide/testing_runbook.md) | Automated tests, linting, manual smoke tests |
| [API Reference](developer_guide/api_reference.md) | Function signatures, parameter types, return values |
| [About](about.md) | Project motivation, tech stack rationale, contact |
