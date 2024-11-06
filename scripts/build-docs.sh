#!/usr/bin/env bash

export TERMINAL_WIDTH=80

set -e
set -x

# build docs/docs_src/getting_started
cd docs/docs_src/getting_started && \
    cookiecutter -f -o mesop --no-input https://github.com/airtai/cookiecutter-fastagency.git && app_type=mesop \
    tree mesop/my_fastagency_app | sed 's/^/        /' > mesop/folder_structure.txt && \
    cookiecutter -f -o fastapi --no-input https://github.com/airtai/cookiecutter-fastagency.git && app_type=fastapi+mesop \
    tree fastapi/my_fastagency_app | sed 's/^/        /' > fastapi/folder_structure.txt && \
    cookiecutter -f -o fastapi_n_nats --no-input https://github.com/airtai/cookiecutter-fastagency.git && app_type=nats+fastapi+mesop \
    tree fastapi_n_nats/my_fastagency_app | sed 's/^/        /' > fastapi_n_nats/folder_structure.txt && \
    cd ../../..


# build docs
cd docs; python docs.py build
