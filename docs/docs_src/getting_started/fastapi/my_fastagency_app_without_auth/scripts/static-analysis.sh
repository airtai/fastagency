#!/usr/bin/env bash
set -e

echo "Running mypy..."
mypy

echo "Running bandit..."
bandit -c pyproject.toml -r my_fastagency_app_without_auth

echo "Running semgrep..."
semgrep scan --config auto --error
