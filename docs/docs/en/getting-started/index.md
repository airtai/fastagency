---
# 0.5 - API
# 2 - Release
# 3 - Contributing
# 5 - Template Page
# 10 - Default
hide:
  - navigation

search:
  boost: 10
---

# Getting Started with FastAgency


<b>The fastest way to bring multi-agent workflows to production.</b>


---

<p align="center">
  <a href="https://github.com/airtai/fastagency/actions/workflows/pipeline.yaml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/pipeline.yaml/badge.svg?branch=main" alt="Test Passing"/>
  </a>

  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/airtai/fastagency" target="_blank">
      <img src="https://coverage-badge.samuelcolvin.workers.dev/airtai/fastagency.svg" alt="Coverage">
  </a>

  <a href="https://www.pepy.tech/projects/fastagency" target="_blank">
    <img src="https://static.pepy.tech/personalized-badge/fastagency?period=month&units=international_system&left_color=grey&right_color=green&left_text=downloads/month" alt="Downloads"/>
  </a>

  <a href="https://pypi.org/project/fastagency" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastagency?label=PyPI" alt="Package version">
  </a>

  <a href="https://pypi.org/project/fastagency" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastagency.svg" alt="Supported Python versions">
  </a>

  <br/>

  <a href="https://github.com/airtai/fastagency/actions/workflows/codeql.yml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/codeql.yml/badge.svg" alt="CodeQL">
  </a>

  <a href="https://github.com/airtai/fastagency/actions/workflows/dependency-review.yaml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/dependency-review.yaml/badge.svg" alt="Dependency Review">
  </a>

  <a href="https://github.com/airtai/fastagency/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/airtai/fastagency.png" alt="License">
  </a>

  <a href="https://github.com/airtai/fastagency/blob/main/CODE_OF_CONDUCT.md" target="_blank">
    <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Code of Conduct">
  </a>

  <a href="https://discord.gg/kJjSGWrknU" target="_blank">
      <img alt="Discord" src="https://img.shields.io/discord/1247409549158121512?logo=discord">
  </a>
</p>

---

## What is FastAgency?

For start, FastAgency is not yet another agentic AI framework. There are many such
frameworks available today, the most popular open-source ones being [**AutoGen**](https://github.com/microsoft/autogen){target="_blank"}, [**CrewAI**](https://www.crewai.com/){target="_blank"}, [**Swarm**](https://github.com/openai/swarm){target="_blank"} and [**LangGraph**](https://github.com/langchain-ai/langgraph){target="_blank"}. FastAgency provides you with a unified programming interface for deploying agentic workflows written in above agentic frameworks in both development and productional settings (current version supports [**AutoGen**](https://github.com/microsoft/autogen){target="_blank"} only, but other frameworks will be supported very soon). With only a few lines of code, you can create a web chat application or REST API service interacting with agents of your choice. If you need to scale-up your workloads, FastAgency can help you deploy a fully distributed system using internal message brokers coordinating multiple machines in multiple datacenters with just a few lines of code changed from your local development setup.

In the rest of this guide, we will walk you through the initial setup and usage of FastAgency, using both development and production environments.

### Supported Runtimes

Currently, the only supported runtime is [**AutoGen**](https://github.com/microsoft/autogen){target="_blank"}, with support for [**CrewAI**](https://www.crewai.com/){target="_blank"}, [**Swarm**](https://github.com/openai/swarm){target="_blank"} and [**LangGraph**](https://github.com/langchain-ai/langgraph){target="_blank"} coming soon.

### Supported User Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [**`ConsoleUI`**](../api/fastagency/ui/console/ConsoleUI.md) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.

- [**Mesop**](https://google.github.io/mesop/){target="_blank"}: Utilize [**`MesopUI`**](../api/fastagency/ui/mesop/MesopUI.md) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

### Supported Network Adapters

FastAgency can use chainable network adapters that can be used to easily create
scalable, production ready architectures for serving your workflows. Currently, we
support the following network adapters:

- [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} via [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"}: Use the [**`FastAPIAdapter`**](../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve your workflow using [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} server. This setup allows you to work your workflows in multiple workers and serve them using the highly extensible and stable ASGI server.

- [**NATS.io**](https://nats.io/){target="_blank"} via [**FastStream**](https://github.com/airtai/faststream){target="_blank"}: Utilize the [**`NatsAdapter`**](../api/fastagency/adapters/nats/NatsAdapter.md) to use [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for highly-scalable, production-ready setup. This interface is suitable for setups in VPN-s or, in combination with the [**`FastAPIAdapter`**](../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve public workflows in an authenticated, secure manner.

## Quick start

We will show you four different setups, two for development and two for production workloads:

- Development setups

    - **Console**: This setup uses console for interactively executing your workflow.
        It is also very useful for automating testing and integration with CI/CD.


    - **Mesop**: This setup uses [**Mesop**](https://google.github.io/mesop/){target="_blank"}
        to build a web application for interacting with our workflow. It supports
        a single-worker deployments only, limiting its scalability. However, it
        is the fastest way to debug your application.

- Production setups

    - **FastAPI + Mesop**: This is fairly scalable setup using [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} to execute your workflows and [**Mesop**](https://google.github.io/mesop/){target="_blank"} for interactive web application. [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} supports execution with multiple workers, with each workflow being executed in the context of a WebSocket connection. [**Mesop**](https://google.github.io/mesop/){target="_blank"} is still limited to a single worker, although there is much less load of it due to workflows being executed in the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} workers.

    - **NATS + FastAPI + Mesop**: This is the most scalable setup using a distributed message broker
        [**NATS.io MQ**](https://nats.io/){target="_blank"}. Workflows are being executed with
        multiple workers that attach to the MQ waiting for initiate workflow messages. Such workers
        can be running on different machines or even different data centers/cloud providers.
        Message queues are highly scalable, but more difficult to integrate with end-clients.
        In order to make such integrations easier, we will connect our [**NATS**](https://nats.io/){target="_blank"}-based message queue with the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} application.


### Project setup

There are two ways to setup you development environment and project:

- [**Recommended**] Using [**Cookiecutter**](../user-guide/cookiecutter/index.md): This creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

- Using virtual environment, such as [venv](https://docs.python.org/3/library/venv.html){target="_blank"}, and a Python package manager, such as [**pip**](https://en.wikipedia.org/wiki/Pip_(package_manager)).



=== "Cookiecutter"

    1. Install Cookiecutter with the following command:
       ```console
       pip install cookiecutter
       ```

    2. Run the `cookiecutter` command:
       ```console
       cookiecutter https://github.com/airtai/cookiecutter-fastagency.git
       ```

    3. Depending on the type of the project, choose the appropriate option in step 3:

        === "Console"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1):
            ```

            This command installs FastAgency with support for the Console interface and the AutoGen framework.

        === "Mesop"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1): 2
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows.

        === "FastAPI + Mesop"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1): 3
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI handling input requests and workflow execution.

        === "NATS + FastAPI + Mesop"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1): 4
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI serving input and independent workers communicating over the NATS.io protocol workflows. This is the most scable setup, recommended for large production workloads.

    4. Executing the `cookiecutter` command will create the following file structure:

        !!! danger "fix this"

        === "Console"
        === "Mesop"
        === "FastAPI + Mesop"
            ```console
            my_fastagency_app/
            ├── .devcontainer
            │   ├── devcontainer.env
            │   ├── devcontainer.json
            │   ├── docker-compose.yml
            │   └── setup.sh
            ├── .github
            │   └── workflows
            │       └── test.yml
            ├── LICENSE
            ├── README.md
            ├── my_fastagency_app
            │   ├── __init__.py
            │   ├── main_1_fastapi.py
            │   ├── main_2_mesop.py
            │   └── workflow.py
            ├── pyproject.toml
            └── tests
                ├── __init__.py
                ├── conftest.py
                └── test_workflow.py
            ```
        === "NATS + FastAPI + Mesop"

    5. To run LLM-based applications, you need an API key for the LLM used. The most commonly used LLM is [OpenAI](https://platform.openai.com/docs/models). To use it, create an [OpenAI API Key](https://openai.com/index/openai-api/) and set it as an environment variable in the terminal using the following command:

        ```console
        export OPENAI_API_KEY=openai_api_key_here
        ```

        If you want to use a different LLM provider, follow [this guide](../user-guide/runtimes/autogen/using_non_openai_models.md).

        Alternatively, you can skip this step and set the LLM API key as an environment variable later in the devcontainer's terminal. If you open the project in [Visual Studio Code](https://code.visualstudio.com/){target="_blank"} using GUI, you will need to manually set the environment variable in the devcontainer's terminal.

    6. Open the generated project in [Visual Studio Code](https://code.visualstudio.com/){target="_blank"} with the following command:
        ```console
        code my_fastagency_app
        ```

    7. Once the project is opened, you will get the following option to reopen it in a devcontainer:

        <img src="./images/reopen-in-container.png" width="600" class="center">

    8. After reopening the project in devcontainer, you can verify that the setup is correct by running the provided tests with the following command:

        ```console
        pytest
        ```

        You should get the following output if everything is correctly setup.
        ```console
        =================================== test session starts ===================================
        platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0
        rootdir: /workspaces/my_fastagency_app
        configfile: pyproject.toml
        plugins: asyncio-0.24.0, anyio-4.6.2.post1
        asyncio: mode=Mode.STRICT, default_loop_scope=None
        collected 1 item

        tests/test_workflow.py .                                                            [100%]

        ==================================== 1 passed in 1.02s ====================================
        ```



=== "env + pip"

    1. To install FastAgency, you will need `pip`, Python’s package installer. We will use a virtual environment to manage dependencies. Execute the following commands to create and activate a virtual environment:

        ```console
        python3.12 -m venv .venv
        source .venv/bin/activate
        ```

    2. Install FastAgency using the following command, based on the interface you want to use:

        === "Console"
            ```console
            pip install "fastagency[autogen]"
            ```

            This command installs FastAgency with support for the Console interface and the AutoGen framework.

        === "Mesop"
            ```console
            pip install "fastagency[autogen,mesop]"
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows.

        === "FastAPI + Mesop"
            ```console
            pip install "fastagency[autogen,mesop,fastapi,server]"
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI handling input requests and workflow execution.

        === "NATS + FastAPI + Mesop"
            ```console
            pip install "fastagency[autogen,mesop,fastapi,server,nats]"
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI serving input and independent workers communicating over the NATS.io protocol workflows. This is the most scable setup, recommended for large production workloads.

-----

### Imports

Depending on the interface you choose, you'll need to import different modules. These imports set up the necessary components for your application:

=== "Console"
    ```python hl_lines="8"
    {!> docs_src/getting_started/main_console.py [ln:1-8] !}
    ```

    For Console applications, import `ConsoleUI` to handle command-line input and output.

=== "Mesop"
    ```python hl_lines="8"
    {!> docs_src/getting_started/main_mesop.py [ln:1-8] !}
    ```

    For Mesop applications, import `MesopUI` to integrate with the Mesop web interface.

=== "FastAPI + Mesop"
    ```python hl_lines="8"
    {!> docs_src/getting_started/fastapi/main_1_fastapi.py [ln:1-9] !}
    ```

    For FastAPI applications, import `FastAPIAdapter` to expose your workflows as REST API.

=== "NATS + FastAPI + Mesop"
    ```python hl_lines="8"
    {!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py [ln:1-9] !}
    ```

### Define Workflow

You need to define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
{! docs_src/getting_started/main_console.py [ln:9-53] !}
```

This code snippet sets up a simple learning chat between a student and a teacher. You define the agents and how they should interact, specifying how the conversation should be summarized.

### Define FastAgency Application

=== "Console"
    Next, define your FastAgency application. This ties together your workflow and the interface you chose:

    ```python hl_lines="1"
    {!> docs_src/getting_started/main_console.py [ln:54] !}
    ```

    For Console applications, use `ConsoleUI` to handle user interaction via the command line.

=== "Mesop"
    Next, define your FastAgency application. This ties together your workflow and the interface you chose:

    ```python hl_lines="1"
    {!> docs_src/getting_started/main_mesop.py [ln:54] !}
    ```

    For Mesop applications, use `MesopUI` to enable web-based interactions.

=== "FastAPI + Mesop"
    In the case of FastAPI application, we will create an `FastAPIAdapter` and then include a router to the `FastAPI` application.
    The adapter will have all REST and Websocket routes for communicating with a client.

    ```python hl_lines="1 4"
    {!> docs_src/getting_started/fastapi/main_1_fastapi.py [ln:55-58] !}
    ```

=== "NATS + FastAPI + Mesop"
    In the case of NATS.io application, we will create an `NatsAdapter` and then
    add it to a `FastAPI` application using the `lifespan` parameter. The adapter
    will have all REST and Websocket routes for communicating with a client.

    ```python hl_lines="5 7"
    {!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py [ln:55-61] !}
    ```

    The `NatsAdapter` requires a running NATS server. The easiest way to start the NATS server is by using [Docker](https://www.docker.com/){target="_blank"}. FastAgency uses the [JetStream](https://docs.nats.io/nats-concepts/jetstream){target="_blank"} feature of NATS and also utilizes authentication.

    ```python hl_lines="1 3 6 11 17"
    {!> docs_src/getting_started/nats_n_fastapi/nats-server.conf [ln:1-23]!}
    ```

    In the above NATS configuration, we define a user called `fastagency`, and its password is read from the environment variable `FASTAGENCY_NATS_PASSWORD`. We also enable JetStream in NATS and configure NATS to serve via the appropriate ports.

### Adapter Chaining

=== "Console"
    Not applicable for this setup as there are no adapters used.

=== "Mesop"
    Not applicable for this setup as there are no adapters used.

=== "FastAPI + Mesop"

    There is an additional specification file for an application using `MesopUI`
    to connect to the `FastAPIAdapter`

    !!! note "main_2_mesop.py"
        ```python hl_lines="7-9 11"
        {!> docs_src/getting_started/fastapi/main_2_mesop.py [ln:1-11] !}
        ```

=== "NATS + FastAPI + Mesop"

    Above, we created NATS.io provider that will start brokers waiting to consume
    initiate workflow messages from the message broker. Now, we create FastAPI
    service interacting with NATS.io provider:

    !!! note "main_2_fastapi.py"
        ```python hl_lines="16-18 21-22"
        {!> docs_src/getting_started/nats_n_fastapi/main_2_fastapi.py [ln:1-22] !}
        ```

    Finally, we create Mesop app communicating with the FastAPI application:

    !!! note "main_3_mesop.py"
        ```python hl_lines="7-9 11"
        {!> docs_src/getting_started/nats_n_fastapi/main_3_mesop.py [ln:1-11] !}
        ```

### Complete Application Code

Please copy and paste the following code into the same folder, using the file names exactly as mentioned below.

=== "Console"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/getting_started/main_console.py !}
        ```
    </details>

=== "Mesop"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/getting_started/main_mesop.py !}
        ```
    </details>

=== "FastAPI + Mesop"

    <details>
        <summary>main_1_fastapi.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/main_1_fastapi.py !}
        ```
    </details>

    <details>
        <summary>main_2_mesop.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/main_2_mesop.py !}
        ```
    </details>

=== "NATS + FastAPI + Mesop"

    <details>
        <summary>nats-server.conf</summary>
        ```python
        {!> docs_src/getting_started/nats_n_fastapi/nats-server.conf !}
        ```
    </details>

    <details>
        <summary>main_1_nats.py</summary>
        ```python
        {!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py !}
        ```
    </details>

    <details>
        <summary>main_2_fastapi.py</summary>
        ```python
        {!> docs_src/getting_started/nats_n_fastapi/main_2_fastapi.py !}
        ```
    </details>

    <details>
        <summary>main_3_mesop.py</summary>
        ```python
        {!> docs_src/getting_started/nats_n_fastapi/main_3_mesop.py !}
        ```
    </details>

### Run Application

Once everything is set up, you can run your FastAgency application using the following command:

=== "Console"

    !!! note "Terminal"
        ```console
        fastagency run
        ```

=== "Mesop"

    The preferred way to run the [**Mesop**](https://google.github.io/mesop/){target="_blank"} application is using a Python WSGI HTTP server like [**Gunicorn**](https://gunicorn.org/){target="_blank"} on Linux and Mac or [**Waitress**](https://docs.pylonsproject.org/projects/waitress/en/stable/){target="_blank"} on Windows.

    === "Cookiecutter"
        !!! note "Terminal"
            ```console
            gunicorn main:app
            ```
    === "env + pip"

        !!! danger "fix it"

        === "Linux/MacOS"

            First, you need to install it using package manager such as `pip` and then run it:

            !!! note "Terminal"
                ```console
                pip install gunicorn
                gunicorn main:app
                ```

        === "Windows"

            First, you need to install it using package manager such as `pip`:

            !!! note "Terminal"
                ```console
                pip install waitress
                waitress-serve --listen=0.0.0.0:8000 main:app
                ```

=== "FastAPI + Mesop"

    !!! danger "fix it"

    In this setup, we need to run **two** commands in **separate** terminal windows:

    - Start **FastAPI** application using uvicorn:
    !!! note "Terminal 1"
        ```
        uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
        ```

    - Start **Mesop** web interface using gunicorn:
    !!! note "Terminal 2"
        ```
        gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
        ```

    !!! danger "Currently not working on **Windows**"
        The above command is currently not working on **Windows**, because gunicorn is not supported. Please use the alternative method below to start the application:
        ```
        pip install waitress
        waitress-serve --listen=0.0.0.0:8888 main_2_mesop:app
        ```

=== "NATS + FastAPI + Mesop"

    !!! danger "fix it"

    In this setup, we need to run **four** commands in **separate** terminal windows:

    - Start **NATS** Docker container:
    !!! note "Terminal 1"
        ```
        docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats-server.conf:/etc/nats/nats-server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats-server.conf
        ```

    - Start **FastAPI** application that provides a conversational workflow:
    !!! note "Terminal 2"
        ```
        uvicorn main_1_nats:app --reload
        ```

    - Start **FastAPI** application integrated with a **NATS** messaging system:
    !!! note "Terminal 3"
        ```
        uvicorn main_2_fastapi:app --host 0.0.0.0 --port 8008 --reload
        ```

    - Start **Mesop** web interface using gunicorn:
    !!! note "Terminal 4"
        ```
        gunicorn main_3_mesop:app -b 0.0.0.0:8888 --reload
        ```

    !!! danger "Currently not working on **Windows**"
        The above command is currently not working on **Windows**, because gunicorn is not supported. Please use the alternative method below to start the application:
        ```
        pip install waitress
        waitress-serve --listen=0.0.0.0:8888 main_3_mesop:app
        ```

### Output

The outputs will vary based on the interface, here is the output of the last terminal starting UI:

=== "Console"
    ```console
    ╭─ Python module file ─╮
    │                      │
    │  🐍 main.py          │
    │                      │
    ╰──────────────────────╯

    ╭─ Importable FastAgency app ─╮
    │                             │
    │  from main import app       │
    │                             │
    ╰─────────────────────────────╯

    ╭─ FastAgency -> user [workflow_started] ──────────────────────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "name": "simple_learning",                                                 │
    │   "description": "Student and teacher                                        │
    │ learning chat",                                                              │
    │   "params": {}                                                               │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you learn about geometry. What subject you would like to          │
    │ explore?:                                                                    │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

    For Console applications, you will see a command-line prompt where you can enter the initial message and interact with your workflow.

=== "Mesop"
    ```console
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8000 (23635)
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
    [2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
    ```

    ![Initial message](./images/chat.png)

=== "FastAPI + Mesop"
    ```console
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
    [2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
    ```

    ![Initial message](./images/chat.png)

=== "NATS + FastAPI + Mesop"

    ```console
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
    [2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
    ```

    ![Initial message](./images/chat.png)

## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, other network provider and other UI frameworks.

---

## Stay in touch

Please show your support and stay in touch by:

- giving our [GitHub repository](https://github.com/airtai/fastagency/){target="_blank"} a star, and

- joining our [Discord server](https://discord.gg/kJjSGWrknU){target="_blank"}

Your support helps us to stay in touch with you and encourages us to
continue developing and improving the framework. Thank you for your
support!

---

## Contributors

Thanks to all of these amazing people who made the project better!

<a href="https://github.com/airtai/fastagency/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=airtai/fastagency"/>
</a>
