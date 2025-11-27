.PHONY: help venv install clean test lint format act check-venv

VENV_DIR := wikienv
PYTHON := python3
PIP := $(VENV_DIR)/bin/pip
PYTHON_VENV := $(VENV_DIR)/bin/python

check-venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Error: Virtual environment is not activated."; \
		echo "Activate with: source $(VENV_DIR)/bin/activate"; \
		exit 1; \
	fi
	@echo "Virtual environment is active: $$VIRTUAL_ENV"

help:
	@echo "Available commands:"
	@echo "  make venv       - Create virtual environment"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Create venv and install dependencies"
	@echo "  make act        - Activate virtual environment"
	@echo "  make clean      - Remove virtual environment and cache files"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code"

venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)"
	@echo "Activate with: source $(VENV_DIR)/bin/activate"

install: check-venv
	@echo "Installing dependencies..."
	pip install -q --upgrade pip setuptools wheel
	pip install -q -r requirements.txt
	@echo "Dependencies installed"

dev: install
	@echo "Development environment ready!"
	@echo "Activate with: source $(VENV_DIR)/bin/activate"

act:
	@bash -c "source $(VENV_DIR)/bin/activate && bash"

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf *.egg-info
	@echo "Cleanup complete"

test: check-venv
	@echo "Running tests..."
	python -m pytest

lint: check-venv
	@echo "Running linting checks..."
	python -m pylint search_wiki_article.py

format: check-venv
	@echo "Formatting code..."
	python -m black search_wiki_article.py
