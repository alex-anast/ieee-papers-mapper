# About

## Motivation

Academic and industrial researchers deal with an overwhelming and ever-growing volume of published research. Finding, categorizing, and tracking relevant papers across multiple domains is tedious manual work that is well-suited to automation.

IEEE Papers Mapper was built to solve this problem end-to-end: automatically fetch papers from the IEEE Xplore API, classify them into research domains using zero-shot NLP, and visualize the results in a live dashboard. The goal is a system that runs unattended, accumulates a classified corpus over time, and provides an at-a-glance view of how research activity is distributed across topics.

## What Makes It a Good Engineering Project

This project is designed to demonstrate production-quality engineering practices applied to a data/ML pipeline:

- **Data validation at every boundary** -- Pydantic models enforce contracts between pipeline stages. Bad data fails fast with a clear exception, never silently propagates.
- **Repository pattern** -- Clean separation between schema management (`Database`) and typed CRUD operations (`PaperRepository`). No raw dictionaries cross the persistence boundary.
- **Lazy-loaded ML model** -- The 700 MB DeBERTa classifier loads on first use, not at import time. This keeps startup fast and tests lightweight.
- **Incremental processing** -- `ProgressTracker` persists pagination state to JSON, so interrupted runs resume where they left off instead of re-fetching from scratch.
- **Custom exception hierarchy** -- `IEEEApiError` and `PaperValidationError` replace silent error swallowing with explicit, catchable error types.
- **Structured logging** -- JSON-formatted logs via `python-json-logger`, ready for ingestion by any log aggregation system.
- **CI/CD** -- GitHub Actions runs `black` and `pytest` on every push. Docker Compose provides a two-service deployment.
- **Comprehensive testing** -- Unit tests cover the pipeline, repository, models, and exceptions. Manual smoke tests are documented in the testing runbook.

## Tech Stack Rationale

| Component | Choice | Why |
|-----------|--------|-----|
| **Language** | Python 3.12 | Standard for data/ML work. Type hints and modern syntax features. |
| **Database** | DuckDB | Embedded analytical database -- no server to manage, fast aggregation queries, zero-config. |
| **NLP** | HuggingFace Transformers (DeBERTa-v3-large) | State-of-the-art zero-shot classification without fine-tuning. Multi-label support out of the box. |
| **Validation** | Pydantic | Declarative data contracts with clear error messages. Field-level constraints. |
| **Dashboard** | Plotly Dash | Python-native interactive web apps without writing JavaScript. |
| **Scheduling** | APScheduler | Lightweight, in-process scheduling with configurable intervals. |
| **CLI** | Click | Composable command groups with built-in help generation. |
| **Logging** | python-json-logger | Structured JSON output, compatible with ELK/Datadog/CloudWatch. |
| **CI** | GitHub Actions | Free for public repos. Runs lint + tests on every push. |
| **Deployment** | Docker Compose | Two-service setup (dashboard + pipeline) with shared volumes. |

## Future Ideas

- Geographic visualization of author affiliations on a world map.
- Citation graph analysis to identify influential papers and research clusters.
- Support for additional academic APIs (Semantic Scholar, arXiv, PubMed).
- Fine-tuned classifier trained on the accumulated labeled corpus.
- REST API layer for programmatic access to the classified paper database.
- Alerting on new papers matching user-defined criteria.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/alex-anast/ieee-papers-mapper/blob/main/LICENSE) file for details.

## Contact

Alexandros Anastasiou -- [anastasioyaa@gmail.com](mailto:anastasioyaa@gmail.com)

GitHub: [alex-anast](https://github.com/alex-anast)
