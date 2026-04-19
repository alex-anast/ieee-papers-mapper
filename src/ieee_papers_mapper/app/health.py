import os
import duckdb
from flask import jsonify
from ieee_papers_mapper.config import config as cfg


def register_health_routes(server):
    @server.route("/health")
    def health():
        return jsonify({"status": "healthy"}), 200

    @server.route("/ready")
    def ready():
        checks = {}

        try:
            if not os.path.exists(cfg.DB_PATH):
                raise FileNotFoundError(cfg.DB_PATH)
            conn = duckdb.connect(cfg.DB_PATH, read_only=True)
            conn.execute("SELECT 1").fetchone()
            conn.close()
            checks["database"] = "ok"
        except Exception as e:
            checks["database"] = str(e)

        checks["api_key"] = "ok" if cfg.IEEE_API_KEY else "missing"

        all_ok = all(v == "ok" for v in checks.values())
        status_code = 200 if all_ok else 503
        payload = {"status": "ready" if all_ok else "not_ready", "checks": checks}
        return jsonify(payload), status_code
