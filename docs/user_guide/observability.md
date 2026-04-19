# Observability

The project exposes Prometheus metrics, structured JSON logs with run correlation IDs, and health check endpoints. In Docker Compose, Prometheus and Grafana are included for out-of-the-box monitoring.

## Health Endpoints

The Dash application exposes two health endpoints on the same port (default 8050):

| Endpoint | Purpose | Success | Failure |
|----------|---------|---------|---------|
| `GET /health` | Liveness probe | `200 {"status": "healthy"}` | Process is dead (no response) |
| `GET /ready` | Readiness probe | `200 {"status": "ready", "checks": {...}}` | `503 {"status": "not_ready", "checks": {...}}` |

The readiness probe checks:
- **Database**: DuckDB file exists and is queryable
- **API key**: `IEEE_API_KEY` environment variable is set

```bash
# Liveness check
curl http://localhost:8050/health

# Readiness check
curl http://localhost:8050/ready
```

Docker Compose uses `/health` for container health checks. Kubernetes deployments can wire `/health` to livenessProbe and `/ready` to readinessProbe.

---

## Prometheus Metrics

The `/metrics` endpoint returns all application metrics in Prometheus text format.

```bash
curl http://localhost:8050/metrics
```

### Pipeline Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `pipeline_runs_total` | Counter | `status` (success/failure) | Total pipeline executions |
| `pipeline_run_duration_seconds` | Histogram | — | Wall time per pipeline run |

### Fetch Stage Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `papers_fetched_total` | Counter | `category` | Papers fetched from IEEE API |
| `api_requests_total` | Counter | `category`, `status` | IEEE API requests (success/error) |
| `api_request_duration_seconds` | Histogram | `category` | API request latency |

### Classification Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `papers_classified_total` | Counter | `category` | Papers classified |
| `classification_duration_seconds` | Histogram | — | Per-paper classification time |

### Database Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `db_operation_duration_seconds` | Histogram | `operation` | Database operation latency |

### Gauges

| Metric | Type | Description |
|--------|------|-------------|
| `papers_in_database` | Gauge | Total papers stored (updated each pipeline run) |
| `papers_unclassified` | Gauge | Papers awaiting classification |
| `last_successful_run_timestamp` | Gauge | Unix timestamp of last successful run |

### Application Info

| Metric | Type | Description |
|--------|------|-------------|
| `ieee_papers_mapper_info` | Info | Application version metadata |

---

## Structured Logging

All log entries are JSON-formatted (via `python-json-logger`) and written to stdout. Each pipeline run generates a unique `run_id` that appears in every log entry for that run, enabling correlation across log lines.

Example log entry:

```json
{
  "timestamp": "2025-01-15T10:30:45.123Z",
  "level": "INFO",
  "name": "ieee_logger",
  "module": "pipeline",
  "function": "run_pipeline",
  "message": "Pipeline run started",
  "run_id": "a1b2c3d4"
}
```

To filter logs for a specific pipeline run:

```bash
ieee-papers run 2>&1 | jq 'select(.run_id == "a1b2c3d4")'
```

---

## Grafana Dashboard

Docker Compose includes a pre-provisioned Grafana instance with a pipeline monitoring dashboard.

### Access

After `docker compose up`, open [http://localhost:3000](http://localhost:3000):
- **Username**: `admin`
- **Password**: `admin`

The "IEEE Papers Pipeline" dashboard is auto-provisioned and available immediately under Dashboards.

### Dashboard Panels

| Panel | Type | What It Shows |
|-------|------|---------------|
| Pipeline Runs | Stat | Total successful and failed pipeline executions |
| Papers in Database | Stat | Current total paper count |
| Unclassified Papers | Stat | Papers awaiting classification |
| API Errors | Stat | Total IEEE API request failures |
| Papers Fetched | Bar gauge | Papers fetched per category |
| Pipeline Duration | Time series | Pipeline run duration (p50, p95) |
| API Latency | Time series | IEEE API request latency by category |
| Classification Latency | Time series | Per-paper classification time (p50, p95) |

---

## Docker Compose Monitoring Stack

The full monitoring stack runs alongside the application:

```yaml
# Start everything including monitoring
docker compose up -d

# Access points:
# Dashboard:   http://localhost:8050
# Prometheus:  http://localhost:9090
# Grafana:     http://localhost:3000
```

| Service | Port | Purpose |
|---------|------|---------|
| `dashboard` | 8050 | Application dashboard + metrics endpoint |
| `prometheus` | 9090 | Metrics scraping and storage (scrapes `/metrics` every 15s) |
| `grafana` | 3000 | Metrics visualization with pre-built dashboards |

### Architecture

```
dashboard:8050/metrics  ──scrape──▶  prometheus:9090  ──query──▶  grafana:3000
```

Prometheus scrapes the dashboard's `/metrics` endpoint every 15 seconds. Grafana reads from Prometheus and renders the pre-provisioned dashboard.

---

## Extending Observability

### Adding Custom Metrics

Define new metrics in `src/ieee_papers_mapper/config/metrics.py`:

```python
from prometheus_client import Counter
my_counter = Counter("my_custom_metric_total", "Description", ["label_name"])
```

Then instrument the relevant code path:

```python
from ieee_papers_mapper.config.metrics import my_counter
my_counter.labels(label_name="value").inc()
```

The metric will automatically appear on `/metrics` and be scraped by Prometheus.

### Alerting

Prometheus alerting rules can be added to `monitoring/prometheus.yml`. For example, to alert when the pipeline hasn't run in 25 hours:

```yaml
rule_files:
  - /etc/prometheus/alert_rules.yml
```

With a corresponding alert rules file:

```yaml
groups:
  - name: pipeline
    rules:
      - alert: PipelineStale
        expr: time() - last_successful_run_timestamp > 90000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pipeline has not run successfully in over 25 hours"
```
