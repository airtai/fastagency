#!/usr/bin/env bash

# coverage run -m pytest -x --ff "$@" || \
# coverage run -m pytest -x --ff "$@" || \
coverage run -m pytest --ff -vv -m "not (anthropic or azure_oai or openai or togetherai or llm)" "$@"
