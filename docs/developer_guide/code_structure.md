# Code Structure

The project is organized as follows:

## Key Directories

- **`app/`**: Contains the web application.
  - `dash_webapp.py`: Launches the Dash app.
  - `callbacks.py`: Defines interactivity for the Dash app.

- **`data/`**: Core data processing pipeline.
  - `get_papers.py`: Fetches data from IEEE Xplore API.
  - `process_papers.py`: Preprocesses raw paper data.
  - `classify_papers.py`: Classifies papers using transformers.
  - `database.py`: Manages SQLite database operations.
  - `pipeline.py`: Streamlines the process of paper classification altogether.

- **`config/`**: Configuration files.
  - `config.py`: Contains configuration variables.
  - `scheduler.py`: Sets up the job scheduler.

- **`tests/`**: Unit tests for validating modules.

## Supporting Files

- **`README.md`**: Project overview and setup instructions.
- **`setup.py`**: Packaging configuration.
- **`mkdocs.yml`**: Style and format of MkDocs documentation.
