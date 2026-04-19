from prometheus_client import Counter, Histogram, Gauge, Info

# Pipeline runs
pipeline_runs = Counter("pipeline_runs_total", "Pipeline executions", ["status"])
pipeline_duration = Histogram("pipeline_run_duration_seconds", "Pipeline run wall time")

# Fetch stage
papers_fetched = Counter(
    "papers_fetched_total", "Papers fetched from IEEE API", ["category"]
)
api_requests = Counter(
    "api_requests_total", "IEEE API requests", ["category", "status"]
)
api_latency = Histogram(
    "api_request_duration_seconds", "IEEE API request latency", ["category"]
)

# Classification stage
papers_classified = Counter(
    "papers_classified_total", "Papers classified", ["category"]
)
classification_latency = Histogram(
    "classification_duration_seconds", "Per-paper classification time"
)

# DB operations
db_operations = Histogram(
    "db_operation_duration_seconds", "Database operation latency", ["operation"]
)

# Gauges
total_papers_gauge = Gauge("papers_in_database", "Total papers stored")
unclassified_gauge = Gauge("papers_unclassified", "Papers awaiting classification")
last_successful_run = Gauge(
    "last_successful_run_timestamp", "Unix timestamp of last successful pipeline run"
)

# Build info
build_info = Info("ieee_papers_mapper", "Application metadata")
build_info.info({"version": "1.0.0"})
