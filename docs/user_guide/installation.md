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

The dashboard will be available at `http://localhost:8050`.
