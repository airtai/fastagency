#!/usr/bin/env bash

export TERMINAL_WIDTH=80

set -e
set -x

# build docs/docs_src/getting_started
cd docs/docs_src/getting_started && \
    rm -rf fastapi/my_fastagency_app/ mesop/my_fastagency_app/ nats_n_fastapi/my_fastagency_app/; \
    rm -rf fastapi/my_fastagency_app_without_auth/ mesop/my_fastagency_app_without_auth/ nats_n_fastapi/my_fastagency_app_without_auth/; \
    cookiecutter -f -o mesop --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=mesop authentication=basic && \
    cd mesop && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o fastapi --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=fastapi+mesop authentication=basic && \
    cd fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o nats_n_fastapi --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=nats+fastapi+mesop authentication=basic && \
    cd nats_n_fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o mesop --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=mesop authentication=none project_name="My FastAgency App Without Auth" && \
    cookiecutter -f -o fastapi --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=fastapi+mesop authentication=none project_name="My FastAgency App Without Auth" && \
    cookiecutter -f -o nats_n_fastapi --no-input https://github.com/airtai/cookiecutter-fastagency.git app_type=nats+fastapi+mesop authentication=none project_name="My FastAgency App Without Auth" && \
    cd ../../..


# build docs
rm -rf docs/docs/en/api docs/docs/en/cli
cd docs; python docs.py build
