#!/usr/bin/env bash

# coverage run -m pytest -x --ff "$@" || \
# coverage run -m pytest -x --ff "$@" || \
coverage run -m pytest --ff "$@"
