# Code Structure

The project follows a Python src-layout with clear separation of concerns.

## Architecture

```
src/ieee_papers_mapper/
    models.py           # Pydantic models: Author, ProcessedPaper, ClassifiedPaper
    exceptions.py       # Custom exception hierarchy
    main.py             # Entry point — starts the scheduler

    config/
        config.py           # Environment-sourced settings and constants
        scheduler.py        # APScheduler wrapper (accepts any callable)
        logging_config.py   # Structured JSON logging setup

    data/
        get_papers.py       # IEEE Xplore API client
        process_papers.py   # Raw API data -> validated ProcessedPaper models
        classify_papers.py  # Zero-shot classification (lazy-loaded DeBERTa)
        database.py         # Connection lifecycle and schema management (DDL)
        repository.py       # CRUD operations with typed Pydantic models
        pipeline.py         # Orchestrates fetch -> process -> store -> classify
    
    app/
        dash_webapp.py      # Plotly Dash dashboard for paper counts by category
```

## Data Flow

```
IEEE API  ->  get_papers()  ->  pd.DataFrame (raw)
                                    |
                            process_papers()  ->  list[ProcessedPaper]
                                    |
                        PaperRepository.insert_full_paper()
                                    |
                        classify_all_papers()  ->  list[ClassifiedPaper]
                                    |
                        PaperRepository.insert_classifications()
```

Each boundary is validated by Pydantic models. Invalid data raises `PaperValidationError` immediately rather than propagating as NaN.

## Key Design Decisions

- **Repository pattern**: `Database` handles connection and schema; `PaperRepository` handles CRUD with typed models.
- **Lazy classifier**: The 700MB DeBERTa model is loaded on first use, not at import time.
- **Custom exceptions**: `IEEEApiError` and `PaperValidationError` replace silent error swallowing.
- **ProgressTracker**: Encapsulates incremental pagination state in a JSON file.
- **Dependency injection**: The scheduler accepts any callable, not a hardcoded pipeline import.

## Supporting Files

- **`Makefile`**: Dev runbook with targets for install, test, lint, db-reset, docker, etc.
- **`pyproject.toml`**: Packaging configuration and dependencies.
- **`Dockerfile` / `docker-compose.yml`**: Two-service deployment (dashboard + pipeline).
- **`mkdocs.yml`**: Documentation site configuration.
