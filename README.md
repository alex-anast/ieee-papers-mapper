# IEEE Papers Mapper

## Overview

IEEE Papers Mapper is a comprehensive tool for retrieving, processing, classifying, and visualizing research papers from the IEEE Xplore API. It automates data ingestion, applies machine learning for classification, and offers interactive dashboards for insights.

## Badges

![PyPI version](https://img.shields.io/pypi/v/ieee-papers-mapper)<br>
![Build Status](https://img.shields.io/github/actions/workflow/status/alex-anast/ieee-papers-mapper/ci.yml)<br>
![Code Coverage](https://img.shields.io/codecov/c/github/alex-anast/ieee-papers-mapper)<br>
![Issues](https://img.shields.io/github/issues/alex-anast/ieee-papers-mapper)<br>
![Last Commit](https://img.shields.io/github/last-commit/alex-anast/ieee-papers-mapper)
![License](https://img.shields.io/github/license/alex-anast/ieee-papers-mapper)<br>

## Table of Contents

- [IEEE Papers Mapper](#ieee-papers-mapper)
  - [Overview](#overview)
  - [Description](#description)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Documentation](#documentation)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [Roadmap](#roadmap)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  - [Contact](#contact)

## Demo

[![Watch the video](https://img.youtube.com/vi/s_osIJvKWCE/0.jpg)](https://youtu.be/s_osIJvKWCE)

## Description

The IEEE Papers Mapper is a comprehensive pipeline designed to automate the retrieval, processing, classification, and visualization of academic papers sourced from the IEEE Xplore digital library. This tool streamlines research management by automatically fetching papers based on user-defined queries, preprocessing the raw data to extract key metadata, and employing an encoder-only machine learning model to classify papers into predefined categories. The results are stored in a robust SQLite database and visualized through a Plotly Dash web app. The project integrates APScheduler for scheduled data retrieval, ensuring that the pipeline remains up-to-date. It is highly configurable, allowing users to define custom thresholds, categories, and schedules, making it a valuable resource for researchers and data professionals aiming to organize vast volumes of academic literature efficiently.

## Key Features

- Automated Data Retrieval: Scheduled fetching of research papers using APScheduler.
- Data Processing: Cleans, formats, and prepares data for analysis.
- Machine Learning Classification: Zero-shot classification using transformer models.
- Interactive Dashboard: Visualize categorized papers and insights using Plotly Dash.

## Installation

### Prerequisites

- Python 3.12+
- Virtual Environment (optional but recommended)
- Required tools: pip, git

### Steps (for Usage)

1. Create a project directory:

    ```bash
    mkdir ~/workspace/my_project
    cd ~/workspace/my_project
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```

3. Install the `pip` package and start using it at will:

    ```bash
    pip install ieee-papers-mapper
    ```

### Steps (for Development)

1. Clone the repository

    ```bash
    git clone https://github.com/alex-anast/ieee-papers-mapper.git
    cd ieee-papers-mapper
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Install the package locally:

    ```bash
    pip install .
    ```

## Usage

### Running the Application

#### Dashboard

To launch the dashboard, run:

```bash
python ieee_papers_mapper/app/dash_webapp.py
```

Visit [http://localhost:8050](http://localhost:8050) to view the dashboard.

#### Data Pipeline

To run the pipeline of retrieving, processing and classifying the papers automatically, execute:

```bash
python ieee_papers_mapper/main.py --days 1
```

NOTE: Currently the scheduler is commented out. The pipeline runs must be executed manually.

### Functionality

- **Data Retrieval:** Automatically fetches new papers based on categories from IEEE Xplore.
- **Data Processing:** Handles missing columns and formats data for classification.
- **Classification:** Uses a DeBERTa-v3 model for zero-shot classification into predefined categories.
- **Data Storage:** Uses SQLite3 for storing the data in an SQL database (scalability, modularity over CSV files).

## Documentation

### Link to Docs

Complete documentation is available at: [https://alex-anast.com/ieee-papers-mapper/](alex-anast.com/ieee-papers-mapper/)

### Code structure

```bash
./ieee-pappers-mapper
├── conftest.py
├── docs                                # MkDocs
│   ├── about.md
│   ├── developer_guide
│   │   ├── api_reference.md
│   │   └── code_structure.md
│   ├── index.md
│   └── user_guide
│       ├── installation.md
│       ├── overview.md
│       └── usage.md
├── LICENSE
├── mkdocs.yml                          # MkDocs config
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.py
├── src
│   └── ieee_papers_mapper
│       ├── app                         # Web App (plotly dash)
│       │   ├── assets
│       │   │   └── styles.css
│       │   ├── callbacks.py
│       │   ├── dash_webapp.py
│       │   └── __init__.py
│       ├── config                      # Config and util files
│       │   ├── config.py
│       │   ├── progress.json
│       │   └── scheduler.py            # Custom scheduler wrapper class
│       ├── data
│       │   ├── classify_papers.py      # Classification
│       │   ├── database.py             # Custom Database wrapper class
│       │   ├── get_papers.py           # Paper retrieval
│       │   ├── __init__.py
│       │   ├── pipeline.py             # Pipeline actions
│       │   └── process_papers.py       # Paper (pre)processing
│       ├── ieee_papers.db
│       ├── __init__.py
│       └── main.py
└── tests
    ├── __init__.py
    ├── test_classify_papers.py
    ├── test_database.py
    ├── test_get_papers.py
    └── test_process_papers.py
```

## Testing

Run the tests with:

`python -m pytest`

### Testing Coverage

- **get_papers.py:** Validates API integration and error handling.
- **process_papers.py:** Ensures data cleaning and formatting.
- **classify_papers.py:** Verifies ML classification accuracy and runtime performance.
- **database.py:** Checks database initialization and CRUD operations.

## Contributing

### Guidelines

- Fork the repository and submit a pull request.
- Adhere to PEP 8 code style.
- Include unit tests for new core functionality.
- Lint with `black` formatter.

## Roadmap

### Future Features

1. Currently `author index terms` is not consistent, and therefore commented out. Fix.
2. Scheduler is not enabled.
3. Add more advanced ML models for classification.
4. Enhance the dashboard with dynamic filtering.

## Actionable TODOs to Turn to Enterprise Level

This project has a solid foundation. To elevate it to a level that showcases enterprise-grade engineering, the following steps should be taken. These focus on scalability, reliability, security, observability, and maintainability.

### 1. Production-Grade Deployment & Scalability

The current project runs locally. The single most impactful step is to make it a deployable, scalable service.

*   **Containerize Everything:**
    *   **Action:** Create a `Dockerfile` for the main application (pipeline + scheduler) and another for the Dash web app. Use a multi-stage build to keep the final images lean. Create a `docker-compose.yml` to orchestrate the services locally.
    *   **Why it shows seniority:** Demonstrates understanding of environment consistency, portability, and managing multi-service applications.

*   **Infrastructure as Code (IaC):**
    *   **Action:** Use Terraform to define the cloud infrastructure needed to run your application. This would include a database instance, a container orchestration service, and the necessary networking and security groups.
    *   **Why it shows seniority:** You are not manually clicking buttons in a cloud console. You are creating reproducible, version-controlled infrastructure, a core tenet of modern DevOps and SRE.

*   **Deploy to the Cloud:**
    *   **Action:** Use the Terraform script to deploy the containerized application to a cloud provider (e.g., AWS, GCP, Azure).
        *   **Database:** Replace SQLite with a managed, production-grade database like **AWS RDS (PostgreSQL)**. This is critical for scalability and reliability.
        *   **Container Orchestration:** Deploy your containers using a service like **AWS ECS (Elastic Container Service)** or **EKS (Elastic Kubernetes Service)**.
    *   **Why it shows seniority:** Shows the ability to take a project from a local machine to a real-world, scalable cloud environment.

### 2. Advanced Architecture & Data Engineering

Refactor the pipeline from a single script into a more robust, event-driven architecture.

*   **Decouple the Pipeline with a Message Queue:**
    *   **Action:** Instead of a monolithic `run_pipeline` function, break it into discrete services that communicate via a message queue (e.g., **AWS SQS** or **RabbitMQ**).
        1.  **Fetcher Service**: Polls the IEEE API and pushes new paper IDs into a "papers_to_process" queue.
        2.  **Processing Service**: Listens to the queue, fetches full paper details, processes them, and stores them in the database.
        3.  **Classifier Service**: After processing, a message is sent to a "papers_to_classify" queue. This service picks it up, runs the ML model, and updates the database.
    *   **Why it shows seniority:** This demonstrates a deep understanding of distributed systems, improving scalability (workers can be scaled independently) and resilience (failed messages can be retried).

*   **Data Validation:**
    *   **Action:** Integrate a data validation library like **Pydantic** or **Great Expectations**. Before inserting data into your database, validate that it conforms to an expected schema (e.g., `publication_year` is a valid year, `title` is a non-empty string).
    *   **Why it shows seniority:** Proactively ensures data quality, preventing "garbage in, garbage out" and making the system more robust.

### 3. Observability and Security

A production system is a black box unless you instrument it.

*   **Structured Logging & Monitoring:**
    *   **Action:**
        1.  Configure your logger to output logs in **JSON format**.
        2.  In your cloud deployment, ship these logs to a centralized logging service (e.g., **AWS CloudWatch** or the ELK stack).
        3.  Add monitoring with **Prometheus** and **Grafana**. Expose key metrics from your application, such as `papers_processed_per_minute`, `api_error_rate`, and `classification_time_seconds`.
    *   **Why it shows seniority:** Demonstrates thinking about how to debug and monitor a system *after* it's deployed.

*   **Security Hardening:**
    *   **Action:** Move the IEEE API key from the `.env` file to a dedicated secrets management service like **AWS Secrets Manager** or **HashiCorp Vault**. The application should fetch the secret at runtime.
    *   **Why it shows seniority:** Shows understanding of enterprise-grade security practices for managing sensitive credentials.

### 4. Documentation

*   **Architectural Design Document:**
    *   **Action:** Create a new document in the `docs` folder explaining the new, event-driven architecture with diagrams.
    *   **Why it shows seniority:** The ability to clearly communicate complex technical designs is a critical skill for senior engineers.

### Known Issues

Limited to 20 API calls/day and to max 200 papers/call, due to IEEE Xplore API restrictions.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Acknowledgments

### Inspiration

This project is a recreated minimal duplicate to my internship at Toyota Motor Europe, Belgium.

### Special Thanks

To my mentors at TME.

## Contact

- Owner: Alexandros Anastasiou
- Email: [anastasioyaa@gmail.com](mailto:anastasioyaa@gmail.com)
