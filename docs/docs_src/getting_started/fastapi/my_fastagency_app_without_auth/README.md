# My FastAgency App Without Auth

This repository contains a [`FastAgency`](https://github.com/airtai/fastagency) application which uses [FastAPI](https://fastapi.tiangolo.com/), and [Mesop](https://google.github.io/mesop/). Below, you'll find a guide on how to run the application.

## Running FastAgency Application

To run this [`FastAgency`](https://github.com/airtai/fastagency) application, follow these steps:

1. To run the `FastAgency` application, you need an API key for any LLM. The most commonly used LLM is [OpenAI](https://platform.openai.com/docs/models). To use it, create an [OpenAI API Key](https://openai.com/index/openai-api/) and set it as an environment variable in the terminal using the following command:

   ```bash
   export OPENAI_API_KEY=paste_openai_api_key_here
   ```

   If you want to use a different LLM provider, follow [this guide](https://fastagency.ai/latest/user-guide/runtimes/autogen/using_non_openai_models/).

   Alternatively, you can skip this step and set the LLM API key as an environment variable later in the devcontainer's terminal. If you open the project in `VSCode` using GUI, you will need to manually set the environment variable in the devcontainer's terminal.

   For [GitHub Codespaces](https://github.com/features/codespaces), you can set the LLM API key as a secret by following [this guide](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/specifying-recommended-secrets-for-a-repository), Or directly as an environment variable in the Codespaces' terminal.

2. Open this folder in [VSCode](https://code.visualstudio.com/) using the following command:

   ```bash
   code .
   ```

   If you are using GUI to open the project in `VSCode`, you will need to manually set the environment variable in the devcontainer's terminal.

   Alternatively, you can open this repository in [GitHub Codespaces](https://github.com/features/codespaces).

3. Press `Ctrl+Shift+P`(for windows/linux) or `Cmd+Shift+P`(for mac) and select the option `Dev Containers: Rebuild and Reopen in Container`. This will open the current repository in a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) using Docker and will install all the requirements to run the example application.

4. The `workflow.py` file defines the autogen workflows. It is imported and used in the files that define the `UI`.

5. The `main_1_fastapi.py` file defines the `FastAPIAdapter`. In a devcontainer terminal(**Terminal 1**), run the following command:

   ```bash
   uvicorn my_fastagency_app_without_auth.deployment.main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
   ```

6. The `main_2_mesop.py` file defines the `MesopUI`. In a new devcontainer terminal(**Terminal 2**), run the following command:

   ```bash
   gunicorn my_fastagency_app_without_auth.deployment.main_2_mesop:app -b 0.0.0.0:8888 --reload
   ```

7. Open the Mesop UI URL [http://localhost:8888](http://localhost:8888) in your browser. You can now use the graphical user interface to start and run the autogen workflow.

## Running tests

This `FastAgency` project includes tests to test the autogen workflow. Run these tests with the following command:

```bash
pytest -s
```

## Docker

This `FastAgency` project includes a Dockerfile for building and running a Docker image. You can build and test-run the Docker image within the devcontainer, as docker-in-docker support is enabled. Follow these steps:

1. In the devcontainer terminal, run the following command to build the Docker image:

   ```bash
   docker build -t deploy_fastagency -f docker/Dockerfile .
   ```

2. Once the Docker image is built, you can run it using the following command:

   ```bash
   docker run --rm -d --name deploy_fastagency -e OPENAI_API_KEY=$OPENAI_API_KEY  -p 8008:8008 -p 8888:8888  deploy_fastagency
   ```

## Deploying with Docker

This `FastAgency` project includes a `fly.toml` file for deployment to [fly.io](https://fly.io/), allowing you to share this project with others using a single URL. If you prefer deploying to another hosting provider, you can use the provided Dockerfile. To deplooy to fly.io, follow these steps:

1. Login into fly.io:

   ```bash
   fly auth login
   ```

2. Launch the fly.io app:

   ```bash
   fly launch --config fly.toml --copy-config --yes
   ```

3. Set necessary LLM API key(for example, OPENAI_API_KEY) as a secret:

   ```bash
   fly secrets set OPENAI_API_KEY=paste_openai_api_key_here
   ```

## What's Next?

Once you’ve experimented with the default workflow in the `workflow.py` file, modify the autogen workflow to define your own workflows and try them out.
