# Usage Guide

This guide explains how to use the IEEE Papers Mapper pipeline and visualize results.

## Running the Pipeline

Fetch, process, and classify new papers:

```bash
python -m ieee_papers_mapper.main --run-pipeline
```

## Running the Web Application

To visualize the results:

```bash
python -m ieee_papers_mapper.app.dash_webapp
```

Open your browser and navigate to `http://127.0.0.1:8050` to interact with the web app.
