# Installation Guide

Follow these steps to set up and run the IEEE Papers Mapper on your local machine.

## Prerequisites

Ensure you have the following installed:

- Python 3.12 or later
- Pip (Python package manager)
- Git

## Installation Steps (User)

1. Create a working directory:

```bash
mkdir my_project
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install `ieee-papers-mapper` pip package:

```bash
pip install ieee-papers-mapper
```

## Installation Steps (Developer)

1. Clone the repository:

```bash
git clone https://github.com/alex-anast/ieee-papers-mapper.git
cd ieee-papers-mapper
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Install the project in editable mode:

```bash
pip install -e .
```

5. Open the web app for visualizing the results. At the start, it is going to be an empty page:

```bash
python ieee_papers_mapper/data/app/dash_webapp.py
```

6. Initiate the sourcing of papers coming in from IEEE Xplore API:

```bash
python ieee_papers_mapper/data/main.py
```
