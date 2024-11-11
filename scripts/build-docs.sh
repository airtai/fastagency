#!/usr/bin/env bash

export TERMINAL_WIDTH=80

set -e
set -x

# build docs/docs_src/getting_started
cd docs/docs_src/getting_started && \
    rm -rf fastapi/my_fastagency_app/ mesop/my_fastagency_app/ nats_n_fastapi/my_fastagency_app/; \
    cookiecutter -f -o mesop --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=mesop && \
    cd mesop && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o fastapi --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=fastapi+mesop && \
    cd fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o nats_n_fastapi --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=nats+fastapi+mesop && \
    cd nats_n_fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cd ../../..


# build docs
rm -rf docs/docs/en/api docs/docs/en/cli
cd docs; python docs.py build
