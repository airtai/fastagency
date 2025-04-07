#!/usr/bin/env bash
set -e

echo "Running mypy..."
mypy

echo "Running bandit..."
bandit -c pyproject.toml -r my_bank_app

echo "Running semgrep..."
semgrep scan --config auto --error
