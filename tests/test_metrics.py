import pytest
import duckdb
from unittest.mock import patch, MagicMock
from prometheus_client import REGISTRY


@pytest.fixture
def flask_client():
    """Create a Flask test client with health routes and /metrics registered."""
    from ieee_papers_mapper.app.dash_webapp import app

    app.server.config["TESTING"] = True
    return app.server.test_client()


def test_health_endpoint(flask_client):
    """GET /health returns 200 with status=healthy."""
    response = flask_client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_ready_endpoint_healthy(flask_client, tmp_path, monkeypatch):
    """GET /ready returns 200 when DB exists and API key is set."""
    db_path = str(tmp_path / "test.duckdb")
    conn = duckdb.connect(db_path)
    conn.close()
    monkeypatch.setattr("ieee_papers_mapper.app.health.cfg.DB_PATH", db_path)
    monkeypatch.setattr("ieee_papers_mapper.app.health.cfg.IEEE_API_KEY", "test_key")
    response = flask_client.get("/ready")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"
    assert data["checks"]["database"] == "ok"
    assert data["checks"]["api_key"] == "ok"


def test_ready_endpoint_missing_db(flask_client, tmp_path, monkeypatch):
    """GET /ready returns 503 when DB file doesn't exist."""
    monkeypatch.setattr(
        "ieee_papers_mapper.app.health.cfg.DB_PATH",
        str(tmp_path / "nonexistent.duckdb"),
    )
    monkeypatch.setattr("ieee_papers_mapper.app.health.cfg.IEEE_API_KEY", "test_key")
    response = flask_client.get("/ready")
    assert response.status_code == 503
    data = response.get_json()
    assert data["status"] == "not_ready"


def test_ready_endpoint_missing_api_key(flask_client, tmp_path, monkeypatch):
    """GET /ready returns 503 when API key is not set."""
    db_path = str(tmp_path / "test.duckdb")
    conn = duckdb.connect(db_path)
    conn.close()
    monkeypatch.setattr("ieee_papers_mapper.app.health.cfg.DB_PATH", db_path)
    monkeypatch.setattr("ieee_papers_mapper.app.health.cfg.IEEE_API_KEY", None)
    response = flask_client.get("/ready")
    assert response.status_code == 503
    data = response.get_json()
    assert data["checks"]["api_key"] == "missing"


def test_metrics_endpoint(flask_client):
    """GET /metrics returns Prometheus text format with expected metric names."""
    response = flask_client.get("/metrics")
    assert response.status_code == 200
    assert response.content_type.startswith("text/plain")
    body = response.data.decode()
    assert "pipeline_runs_total" in body
    assert "papers_fetched_total" in body
    assert "api_request_duration_seconds" in body
    assert "classification_duration_seconds" in body
    assert "papers_in_database" in body
    assert "ieee_papers_mapper_info" in body


def test_metrics_module_defines_all_metrics():
    """Verify all expected metrics are defined in the metrics module."""
    from ieee_papers_mapper.config import metrics as m

    assert hasattr(m, "pipeline_runs")
    assert hasattr(m, "pipeline_duration")
    assert hasattr(m, "papers_fetched")
    assert hasattr(m, "api_requests")
    assert hasattr(m, "api_latency")
    assert hasattr(m, "papers_classified")
    assert hasattr(m, "classification_latency")
    assert hasattr(m, "db_operations")
    assert hasattr(m, "total_papers_gauge")
    assert hasattr(m, "unclassified_gauge")
    assert hasattr(m, "last_successful_run")
    assert hasattr(m, "build_info")
