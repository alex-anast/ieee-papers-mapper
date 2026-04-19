SHELL := /bin/bash
.DEFAULT_GOAL := help

VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
TORCH_INDEX := https://download.pytorch.org/whl/cpu

.PHONY: help venv install lint format test test-verbose clean db-reset dash-smoke check

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment
	python3 -m venv $(VENV_DIR)
	@echo "Virtualenv created at $(VENV_DIR)"

install: venv ## Install all dependencies into the venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt --extra-index-url $(TORCH_INDEX)
	$(PIP) install -e .
	@echo "All dependencies installed."

lint: ## Run black in check mode
	$(PYTHON) -m black --check src/ tests/

format: ## Auto-format code with black
	$(PYTHON) -m black src/ tests/

test: ## Run tests with pytest
	$(PYTHON) -m pytest tests/ -v --tb=short

test-verbose: ## Run tests with full output
	$(PYTHON) -m pytest tests/ -v --tb=long -s

db-reset: ## Delete and recreate the SQLite database
	rm -f src/ieee_papers_mapper/ieee_papers.duckdb
	$(PYTHON) -c "from ieee_papers_mapper.data.database import Database; \
		db = Database(name='ieee_papers', filepath='src/ieee_papers_mapper'); \
		db.initialise(); db.close(); print('Database recreated.')"

dash-smoke: ## Start dashboard, verify it responds, then stop it
	@echo "Starting Dash server..."
	@$(PYTHON) -m ieee_papers_mapper.app.dash_webapp & \
		DASH_PID=$$!; \
		sleep 3; \
		STATUS=$$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8050); \
		kill $$DASH_PID 2>/dev/null; \
		if [ "$$STATUS" = "200" ]; then \
			echo "Dash smoke test PASSED (HTTP $$STATUS)"; \
		else \
			echo "Dash smoke test FAILED (HTTP $$STATUS)"; exit 1; \
		fi

clean: ## Remove venv, caches, and build artifacts
	rm -rf $(VENV_DIR)
	rm -rf __pycache__ src/**/__pycache__ tests/__pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info src/*.egg-info
	rm -rf build dist
	@echo "Cleaned."

check: lint test ## Run lint + tests (preflight check)
	@echo "All checks passed."
