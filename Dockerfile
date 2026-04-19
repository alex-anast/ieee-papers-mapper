FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifests first for better layer caching
COPY requirements.txt pyproject.toml ./

# Install dependencies (CPU-only torch)
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# Copy source tree and install the package in editable mode
COPY src/ ./src/
RUN pip install --no-cache-dir -e .

# Default: run the Dash dashboard
CMD ["python", "-m", "ieee_papers_mapper.app.dash_webapp"]
