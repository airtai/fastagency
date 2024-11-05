---
# 0.5 - API
# 2 - Release
# 3 - Contributing
# 5 - Template Page
# 10 - Default
# hide:
#   - navigation

search:
  boost: 10
---

# Getting Started with FastAgency


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

- [**Recommended**] Using [**Cookiecutter**](../cookiecutter/index.md): This creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

- Using virtual environment, such as [venv](https://docs.python.org/3/library/venv.html){target="_blank"}, and a Python package manager, such as [**pip**](https://en.wikipedia.org/wiki/Pip_(package_manager)).


Let's see how to setup project using cookiecutter:

{! docs/en/user-guide/cookiecutter/index.md[ln:6-226] !}

-----

### Workflow Development

#### Define the Workflow

You need to define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
{! docs_src/getting_started/workflow.py [ln:1-51] !}
```

This code snippet sets up a simple learning chat between a student and a teacher. You define the agents and how they should interact, specifying how the conversation should be summarized.

#### Run and Debug the Workflow

To ensure that the workflow we have defined is working properly, we can test it locally using MesopUI. The code below imports the defined workflow and sets up MesopUI:

```python
{! docs_src/getting_started/main_mesop.py [ln:1-8] !}
```

Run MesopUI locally with the following command:

=== "Linux/MacOS"
    !!! note "Terminal"
        ```console
        gunicorn main_mesop:app
        ```

=== "Windows"
    !!! note "Terminal"
        ```console
        waitress-serve --listen=0.0.0.0:8000 main_mesop:app
        ```

Open the MesopUI URL [http://localhost:8000](http://localhost:8000) in your browser. You can now use the graphical user interface to start, run, test and debug the autogen workflow manually.

#### Run Workflow Tests

We can also use pytest to test the autogen workflow automatically, instead of manually testing it using MesopUI.

```python
{! docs_src/getting_started/test_workflow.py [ln:1-31] !}
```

Run the test with the following command:

```console
pytest
```

Running the test could take up to 30 seconds, depending on latency and throughput of OpenAI (or other LLM providers).

### Workflow Deployment

#### Imports

Depending on the interface you choose, you'll need to import different modules. These imports set up the necessary components for your application:

=== "Console"
    ```python hl_lines="2"
    {!> docs_src/getting_started/main_console.py [ln:1-4] !}
    ```

    For Console applications, import `ConsoleUI` to handle command-line input and output.

=== "Mesop"
    ```python hl_lines="2"
    {!> docs_src/getting_started/main_mesop.py [ln:1-4] !}
    ```

    For Mesop applications, import `MesopUI` to integrate with the Mesop web interface.

=== "FastAPI + Mesop"
    ```python hl_lines="3"
    {!> docs_src/getting_started/fastapi/main_1_fastapi.py [ln:1-5] !}
    ```

    For FastAPI applications, import `FastAPIAdapter` to expose your workflows as REST API.

=== "NATS + FastAPI + Mesop"
    ```python hl_lines="5"
    {!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py [ln:1-7] !}
    ```

#### Define FastAgency Application

=== "Console"
    Next, define your FastAgency application. This ties together your workflow and the interface you chose:

    ```python hl_lines="1"
    {!> docs_src/getting_started/main_console.py [ln:7] !}
    ```

    For Console applications, use `ConsoleUI` to handle user interaction via the command line.

=== "Mesop"
    Next, define your FastAgency application. This ties together your workflow and the interface you chose:

    ```python hl_lines="1"
    {!> docs_src/getting_started/main_mesop.py [ln:7] !}
    ```

    For Mesop applications, use `MesopUI` to enable web-based interactions.

=== "FastAPI + Mesop"
    In the case of FastAPI application, we will create an `FastAPIAdapter` and then include a router to the `FastAPI` application.
    The adapter will have all REST and Websocket routes for communicating with a client.

    ```python hl_lines="1 4"
    {!> docs_src/getting_started/fastapi/main_1_fastapi.py [ln:8-11] !}
    ```

=== "NATS + FastAPI + Mesop"
    In the case of NATS.io application, we will create an `NatsAdapter` and then
    add it to a `FastAPI` application using the `lifespan` parameter. The adapter
    will have all REST and Websocket routes for communicating with a client.

    ```python hl_lines="5 7"
    {!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py [ln:10-16] !}
    ```

    The `NatsAdapter` requires a running NATS server. The easiest way to start the NATS server is by using [Docker](https://www.docker.com/){target="_blank"}. FastAgency uses the [JetStream](https://docs.nats.io/nats-concepts/jetstream){target="_blank"} feature of NATS and also utilizes authentication.

    ```python hl_lines="1 3 6 11 17"
    {!> docs_src/getting_started/nats_n_fastapi/nats-server.conf [ln:1-23]!}
    ```

    In the above NATS configuration, we define a user called `fastagency`, and its password is read from the environment variable `FASTAGENCY_NATS_PASSWORD`. We also enable JetStream in NATS and configure NATS to serve via the appropriate ports.

#### Adapter Chaining

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
        <summary>workflow.py</summary>
        ```python
        {!> docs_src/getting_started/workflow.py !}
        ```
    </details>

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/getting_started/main_console.py !}
        ```
    </details>

=== "Mesop"

    <details>
        <summary>workflow.py</summary>
        ```python
        {!> docs_src/getting_started/workflow.py !}
        ```
    </details>

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/getting_started/main_mesop.py !}
        ```
    </details>

=== "FastAPI + Mesop"

    <details>
        <summary>workflow.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/workflow.py !}
        ```
    </details>

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
        <summary>workflow.py</summary>
        ```python
        {!> docs_src/getting_started/nats_n_fastapi/workflow.py !}
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

        First, install the package using package manager such as `pip` and then run it:

        === "Linux/MacOS"
            !!! note "Terminal"
                ```console
                pip install gunicorn
                gunicorn main:app
                ```

        === "Windows"
            !!! note "Terminal"
                ```console
                pip install waitress
                waitress-serve --listen=0.0.0.0:8000 main:app
                ```

=== "FastAPI + Mesop"

    In this setup, we need to run **two** commands in **separate** terminal windows:

    === "Cookiecutter"

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

    === "env + pip"

        First, install the package using package manager such as `pip` and then run it:

        === "Linux/MacOS"

            - Start **FastAPI** application using uvicorn:
            !!! note "Terminal 1"
                ```
                pip install uvicorn
                uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
                ```

            - Start **Mesop** web interface using gunicorn:
            !!! note "Terminal 2"
                ```
                pip install gunicorn
                gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
                ```

        === "Windows"

            - Start **FastAPI** application using uvicorn:
            !!! note "Terminal 1"
                ```
                pip install uvicorn
                uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
                ```

            - Start **Mesop** web interface using waitress:
            !!! note "Terminal 2"
                ```
                pip install waitress
                waitress-serve --listen=0.0.0.0:8888 main_2_mesop:app
                ```

=== "NATS + FastAPI + Mesop"

    === "Cookiecutter"

        The **NATS** docker container is started automatically by Cookiecutter for this setup. In this setup, we need to run **three** commands in **separate** terminal windows:

        - Start **FastAPI** application that provides a conversational workflow:
        !!! note "Terminal 1"
            ```
            uvicorn main_1_nats:app --reload
            ```

        - Start **FastAPI** application integrated with a **NATS** messaging system:
        !!! note "Terminal 2"
            ```
            uvicorn main_2_fastapi:app --host 0.0.0.0 --port 8008 --reload
            ```

        - Start **Mesop** web interface using gunicorn:
        !!! note "Terminal 3"
            ```
            gunicorn main_3_mesop:app -b 0.0.0.0:8888 --reload
            ```

    === "env + pip"

        First, install the package using package manager such as `pip` and then run it. In this setup, we need to run **four** commands in **separate** terminal windows:

        === "Linux/MacOS"

            - Start **NATS** Docker container:
            !!! note "Terminal 1"
                ```
                docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats-server.conf:/etc/nats/nats-server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats-server.conf
                ```

            - Start **FastAPI** application that provides a conversational workflow:
            !!! note "Terminal 2"
                ```
                pip install uvicorn
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
                pip install gunicorn
                gunicorn main_3_mesop:app -b 0.0.0.0:8888 --reload
                ```

        === "Windows"

            - Start **NATS** Docker container:
            !!! note "Terminal 1"
                ```
                docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats-server.conf:/etc/nats/nats-server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats-server.conf
                ```

            - Start **FastAPI** application that provides a conversational workflow:
            !!! note "Terminal 2"
                ```
                pip install uvicorn
                uvicorn main_1_nats:app --reload
                ```

            - Start **FastAPI** application integrated with a **NATS** messaging system:
            !!! note "Terminal 3"
                ```
                uvicorn main_2_fastapi:app --host 0.0.0.0 --port 8008 --reload
                ```

            - Start **Mesop** web interface using waitress:
            !!! note "Terminal 4"
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

### Building the Docker Image

If you created the project using Cookiecutter, then building the Docker image is as simple as running the provided script, as shown below:

```console
./scripts/build_docker.sh
```

Alternatively, you can use the following command to build the Docker image:

```console
docker build -t deploy_fastagency -f docker/Dockerfile --progress plain .
```

### Running the Docker Image

Similarly, running the Docker container is as simple as running the provided script, as shown below:

```console
./scripts/run_docker.sh
```

Alternatively, you can use the following command to run the Docker container using the Docker image built in the previous step:

```console
docker run -d --name deploy_fastagency -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8888:8888  deploy_fastagency
```

### Deploying to Fly.io

If you created the project using Cookiecutter, there is a built-in script to deploy your workflow to [**Fly.io**](https://fly.io/). Run it as shown below:

```console
./scripts/deploy_to_fly_io.sh
```

Alternatively, you can run the following commands one by one to deploy your workflow to [**Fly.io**](https://fly.io/):

```console
fly auth login

fly launch --config fly.toml --copy-config --yes

fly secrets set OPENAI_API_KEY=$OPENAI_API_KEY
```
