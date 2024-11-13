#!/usr/bin/env bash

# taken from: https://jaredkhan.com/blog/mypy-pre-commit

# A script for running static analysis checks on a Python project,
# with all its dependencies installed.

set -o errexit

# Change directory to the project root directory.
cd "$(dirname "$0")"/..

# Install the dependencies.
# Note that this can take seconds to run.
pip install --editable ".[dev]" \
 --retries 1 \
 --no-input \
 --quiet

# Run static analysis checks.
./scripts/static-analysis.sh
