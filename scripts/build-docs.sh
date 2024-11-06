#!/usr/bin/env bash

export TERMINAL_WIDTH=80

set -e
set -x

cookiecutter -o docs/docs_src/getting_started/mesop -f  --no-input --config-file docs/docs_src/getting_started/mesop/cookiecutter.json  https://github.com/airtai/cookiecutter-fastagency.git  && \
cookiecutter -o docs/docs_src/getting_started/fastapi -f  --no-input --config-file docs/docs_src/getting_started/fastapi/cookiecutter.json  https://github.com/airtai/cookiecutter-fastagency.git && \
cookiecutter -o docs/docs_src/getting_started/nats_n_fastapi -f  --no-input --config-file docs/docs_src/getting_started/nats_n_fastapi/cookiecutter.json  https://github.com/airtai/cookiecutter-fastagency.git && \
cd docs; python docs.py build
