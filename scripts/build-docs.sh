#!/usr/bin/env bash

export TERMINAL_WIDTH=80

set -e
set -x

# build docs/docs_src/getting_started
cd docs/docs_src/getting_started/no_auth/ && \
    rm -rf fastapi/my_fastagency_app/ mesop/my_fastagency_app/ nats_n_fastapi/my_fastagency_app/; \
    cookiecutter -f -o mesop --no-input https://github.com/ag2ai/cookiecutter-fastagency.git app_type=mesop authentication=none && \
    cd mesop && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o fastapi --no-input https://github.com/ag2ai/cookiecutter-fastagency.git app_type=fastapi+mesop authentication=none && \
    cd fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o nats_n_fastapi --no-input https://github.com/ag2ai/cookiecutter-fastagency.git app_type=nats+fastapi+mesop authentication=none && \
    cd nats_n_fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cd ../../../..


cd docs/docs_src/getting_started/basic_auth/ && \
    rm -rf fastapi/my_fastagency_app/ mesop/my_fastagency_app/ nats_n_fastapi/my_fastagency_app/; \
    cookiecutter -f -o mesop --no-input https://github.com/ag2ai/cookiecutter-fastagency.git app_type=mesop authentication=basic && \
    cd mesop && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o fastapi --no-input https://github.com/ag2ai/cookiecutter-fastagency.git app_type=fastapi+mesop authentication=basic && \
    cd fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cookiecutter -f -o nats_n_fastapi --no-input https://github.com/ag2ai/cookiecutter-fastagency.git app_type=nats+fastapi+mesop authentication=basic && \
    cd nats_n_fastapi && tree --noreport --dirsfirst my_fastagency_app > folder_structure.txt && cd .. && \
    cd ../../../..

# build docs/docs_src/user_guide/dependency_injection
cd docs/docs_src/user_guide/dependency_injection && \
    rm -rf mesop/my_bank_app/; \
    cookiecutter -f -o mesop --no-input https://github.com/ag2ai/cookiecutter-fastagency.git project_name="My Bank App" app_type=mesop authentication=none && \
    cd mesop && tree --noreport --dirsfirst my_bank_app > folder_structure.txt && cd .. && \
    cp workflow.py mesop/my_bank_app/my_bank_app
    cd ../../../..

# build docs
rm -rf docs/docs/en/api docs/docs/en/cli
cd docs; python docs.py build
