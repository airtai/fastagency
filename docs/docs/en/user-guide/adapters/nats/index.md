# Nats.io

The [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) in FastAgency enables seamless integration of your workflows with the [**Nats.io MQ**](https://nats.io/){target="_blank"} message broker, providing a scalable and flexible solution for building [**distributed**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"} applications.

## Use Cases

When to Use the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md):

- **High User Demand**: If you need to scale beyond what [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} of the [**FastAPIAdapter**](../fastapi/index.md) can achieve, you can use [**Nats.io**](https://nats.io/){target="_blank"} with a [**message queue**](https://en.wikipedia.org/wiki/Message_queue){target="_blank"} and [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} to consume and produce messages. This distributed message-queue architecture allows scaling not only across multiple workers but also across multiple machines and clusters.

- [**Observability**](https://en.wikipedia.org/wiki/Observability_(software)){target="_blank"}: If you need the ability to **audit workflow executions** both in realtime and retrospectively, the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) provides the necessary infrastructure to enable this feature.

## Architecture Overview

The following diagram illustrates the high-level architecture of an application using the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) with [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md) as its frontend:


![Mesop Nats](../images/mesop_nats.png)

The system consists of two main components:

### Mesop Client App

This application serves as the frontend interface for the system. It includes:

- [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md): A friendly web interface for users to interact with the workflows. It facilitates the communication with the user and the [**`NatsProvider`**](../../../api/fastagency/adapters/nats/NatsProvider.md).
- **Nats Provider**: The [**Nats.io MQ**](https://nats.io/){target="_blank"} message broker responsible for handling message communication between different parts of the system.

This application handles all client interactions and presents the results back to the user.

### Nats App

This application forms the backend of the system and consists of:

- **AutoGen Workflows**: The workflows defined using the [**AutoGen**](https://microsoft.github.io/autogen){target="_blank"} framework. They are executed by the workers in the Nats Adapter.
- [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md): Communicates with AutoGen, and makes the workflow messages available on corresponding [**Nats topics**](https://docs.nats.io/nats-concepts/subjects){target="_blank"}.


Now, it's time to see the Nats Adapter using FastAgency in action. Let's dive into an example and learn how to use it!

## Installation

Before getting started, ensure that FastAgency is installed with support for the [**AutoGen**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime, along with the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md), **fastapi**, **server** and **nats** submodules by running the following command:

```bash
pip install "fastagency[autogen,mesop,fastapi,server,nats]"
```

This command installs FastAgency with support for both the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md) and [**console**](../../../api/fastagency/ui/console/ConsoleUI.md) interfaces for AutoGen workflows and the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) for workflow execution.

Alternatively, you can use [**Cookiecutter**](../../cookiecutter/index.md), which is the preferred method. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

## Example: Student and Teacher Learning Chat

In this example, we'll create a simple learning [**chatbot**](https://en.wikipedia.org/wiki/Chatbot){target="_blank"} where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll use [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md) for the web interface and the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) for workflow execution.

### Step-by-Step Breakdown

#### 1. **Define Workflow**

Define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's an example workflow definition:

```python
{!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/my_fastagency_app/workflow.py [ln:1-47] !}
```

#### 2. **Import Required Modules**

Next, import the required modules from the **FastAgency**. These imports provide the essential building blocks for integrating [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md). Additionally, import the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) class for workflow execution.

```python hl_lines="4"
{!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py [ln:1-7] !}
```

#### 3. **Configure the Nats Adapter**

Create an instance of the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) and pass your workflow to it. The adapter will handle the communication with the [**`NatsProvider`**](../../../api/fastagency/adapters/nats/NatsProvider.md) and distribute workflow execution to the workers.

```python
{!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py [ln:9-13] !}
```

#### 4. **Define FastAgency Application**

Create a [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) and then add it to a [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} application using the [**lifespan parameter**](https://fastapi.tiangolo.com/advanced/events/){target="_blank"}. The adapter will have all [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} and [**WebSocket**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"} routes for communicating with a client.

```python
{!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py [ln:15] !}
```

#### 5. **Nats server setup**

The `NatsAdapter` requires a running NATS server. The easiest way to start the NATS server is by using [**Docker**](https://www.docker.com/){target="_blank"}. FastAgency leverages the [**JetStream**](https://docs.nats.io/nats-concepts/jetstream){target="_blank"} feature of NATS and also utilizes authentication.

```python hl_lines="1 3 8 14"
{!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/.devcontainer/nats_server.conf !}
```

In the above Nats configuration, we define a user called `fastagency`, and its password is read from the environment variable `FASTAGENCY_NATS_PASSWORD`. We also enable JetStream in Nats and configure Nats to serve via the appropriate ports.

### Complete Application Code

Please copy and paste the following code into the same folder, using the file names exactly as mentioned below.

<details>
    <summary>nats_server.conf</summary>
    ```python
    {!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/.devcontainer/nats_server.conf !}
    ```
</details>

<details>
    <summary>workflow.py</summary>
    ```python
    {!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/my_fastagency_app/workflow.py !}
    ```
</details>

<details>
    <summary>main_1_nats.py</summary>
    ```python
    {!> docs_src/getting_started/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py !}
    ```
</details>

<details>
    <summary>main_2_mesop.py</summary>
    ```python
    {!> docs_src/getting_started/nats_n_fastapi/main_2_mesop.py !}
    ```
</details>

### Run Application

=== "Cookiecutter"

    The **NATS** docker container is started automatically by Cookiecutter for this setup. In this setup, we need to run **two** commands in **separate** terminal windows:

    - Start **FastAPI** application that provides a conversational workflow:
    !!! note "Terminal 1"
        ```
        uvicorn main_1_nats:app --reload
        ```

    - Start **Mesop** web interface using gunicorn:
    !!! note "Terminal 2"
        ```
        gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
        ```

=== "env + pip"

    First, install the package using package manager such as `pip` and then run it. In this setup, we need to run **three** commands in **separate** terminal windows:

    === "Linux/MacOS"

        - Start **NATS** Docker container:
        !!! note "Terminal 1"
            ```
            docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats_server.conf:/etc/nats/nats_server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats_server.conf
            ```

        - Start **FastAPI** application that provides a conversational workflow:
        !!! note "Terminal 2"
            ```
            pip install uvicorn
            uvicorn main_1_nats:app --reload
            ```

        - Start **Mesop** web interface using gunicorn:
        !!! note "Terminal 3"
            ```
            pip install gunicorn
            gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
            ```

    === "Windows"

        - Start **NATS** Docker container:
        !!! note "Terminal 1"
            ```
            docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats_server.conf:/etc/nats/nats_server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats_server.conf
            ```

        - Start **FastAPI** application that provides a conversational workflow:
        !!! note "Terminal 2"
            ```
            pip install uvicorn
            uvicorn main_1_nats:app --reload
            ```

        - Start **Mesop** web interface using waitress:
        !!! note "Terminal 3"
            ```
            pip install waitress
            waitress-serve --listen=0.0.0.0:8888 main_2_mesop:app
            ```

### Output

The outputs will vary based on the interface. Here is the output of the last terminal starting the UI:

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

![Initial message](../../getting-started/images/chat.png)

The [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) in FastAgency provides a powerful and flexible way to integrate your workflows with the [**Nats.io**](https://nats.io/){target="_blank"} message broker. By leveraging the scalability and distributed architecture of Nats, you can build highly scalable and production-ready applications. With its easy-to-use API and seamless integration with the [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md), the `NatsAdapter` simplifies the development process while enabling advanced features like conversation auditing.
