# FastAPI + Nats.io

Combining the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) in FastAgency provides the most scalable setup. It harnesses the power of the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework to build and expose workflows as [**REST APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} while utilizing the [**Nats.io**](https://nats.io/){target="_blank"} message broker for scalable and asynchronous communication. This setup is **preferred** for running large workloads in production.

## Use Cases

This section outlines the scenarios where it is particularly beneficial to combine the `FastAPIAdapter` and `NATSAdapter`.

When to Use the `FastAPIAdapter` and `NATSAdapter` Together:

- **High User Demand**: If you need to scale beyond what [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} of the [**FastAPIAdapter**](../fastapi/index.md) can achieve, you can use [**Nats.io**](https://nats.io/){target="_blank"} with a [**message queue**](https://en.wikipedia.org/wiki/Message_queue){target="_blank"} and [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} to consume and produce messages. This distributed message-queue architecture allows scaling not only across multiple workers but also across multiple machines and clusters.

- [**Observability**](https://en.wikipedia.org/wiki/Observability_(software)){target="_blank"}: If you need the ability to **audit workflow executions** both in realtime and retrospectively, the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) provides the necessary infrastructure to enable this feature.

- **Security features of FastAPI**: If you want to leverage the [**security features**](https://fastapi.tiangolo.com/tutorial/security){target="_blank"} of FastAPI, such as authentication, authorization, along with the [**distributed architecture**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"} of NATS, this setup is the most suitable option. Please check the [**securing your FastAPIAdapter**](../fastapi/security.md) documentation for more information.

## Architecture Overview

The following section presents high-level architecture diagrams for the two available setups using the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) together with:

- [**Mesop**](https://google.github.io/mesop/){target="_blank"} client using [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md), and

- Custom [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} and [**WebSocket**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"} client

=== "Mesop"

    ![Mesop FastAPI](../images/mesop_fastapi_nats.png)

    The system is composed of three main components:

    #### 1. Mesop Client App

    This application serves as the frontend interface for the system. It includes:

    - [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md): A friendly web interface for users to interact with the workflows. It facilitates the communication with the user and the [**`FastAPIProvider`**](../../../api/fastagency/adapters/fastapi/FastAPIProvider.md).
    - [**`FastAPIProvider`**](../../../api/fastagency/adapters/fastapi/FastAPIProvider.md): A component that facilitates communication between the Mesop client and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

=== "Custom REST API and WebSocket"

    ![Mesop FastAPI](../images/custom_fastapi_nats.png)

    The system is composed of three main components:

    #### 1. Custom Client App

    This application serves as the frontend interface for the system. It includes:

    - **Custom Client**: A client application built in a different language, (e.g., [**HTML**](https://en.wikipedia.org/wiki/HTML){target="_blank"}/[**JavaScript**](https://en.wikipedia.org/wiki/JavaScript){target="_blank"}, [**Go**](https://go.dev/){target="_blank"}, [**Java**](https://www.java.com/en/){target="_blank"}, etc.) that  facilitates communication between the user and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

    This application handles all interactions with the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and presents the results back to the user.

#### 2. FastAPI App

This application is part of our system's backend and consists of:

- [**`NatsProvider`**](../../../api/fastagency/adapters/nats/NatsProvider.md): Responsible for connecting to the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md), receiving workflow initiation messages, and distributing them to the workers for execution.

- [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md): This component communicates with `NatsProvider`, and implements routes and websocket for FastAPI.

- [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"}: Provides the infrastructure for building and exposing [**AG2**](https://docs.ag2.ai/){target="_blank"} workflows via [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

#### 3. Nats App

This application is also part of our system's backend and consists of:

- [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md): This adapter connects to the `NatsProvider` and is responsible for communicating with AutoGen workflows.

- **AutoGen Workflows**: These workflows, defined using the AutoGen framework, embody the core logic and behavior of your application. They leverage agents to perform various tasks and accomplish specific goals.

This architecture promotes a clear separation of concerns between the user interface, the API layer, and the workflow execution logic, enhancing modularity and maintainability. The [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework provides a user-friendly and efficient [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}, while the `NATSAdapter`, combined with the [**Nats.io**](https://nats.io/){target="_blank"} message broker, ensures scalability and asynchronous communication.

=== "Mesop"


=== "Custom REST API and WebSocket"

    #### Building Custom Client Applications

    For details on building a custom client that interacts with the FastAPI backend, check out the guide [**here**](../fastapi/index.md#building-custom-client-applications). It covers the **routes, message types, and integration steps in detail**, helping you set up seamless communication with FastAPI backend.

Now, it's time to see the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) in action together. Let's dive into an example and learn how to use it!



## Installation

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**.

=== "Mesop"

    Before getting started, ensure that FastAgency is installed with support for the [**AG2**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime, along with the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md), **fastapi**, **server**, and **nats** submodules by running the following command:

    ```bash
    pip install "fastagency[autogen,mesop,fastapi,server,nats]"
    ```

    This command installs FastAgency with support for both the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md) and [**console**](../../../api/fastagency/ui/console/ConsoleUI.md) interfaces for [**AG2**](https://docs.ag2.ai/){target="_blank"} workflows, but with [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} serving input requests and independent workers communicating over [**Nats.io**](https://nats.io/){target="_blank"} protocol running workflows.

=== "Custom REST API and WebSocket"

    Before getting started, ensure that FastAgency is installed with support for the [**AG2**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime, along with the **fastapi**, **server**, and **nats** submodules by running the following command:

    ```bash
    pip install "fastagency[autogen,fastapi,server,nats]"
    ```

    This command installs FastAgency, but with [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} serving input requests and independent workers communicating over [**Nats.io**](https://nats.io/){target="_blank"} protocol running workflows.

## Example: Student and Teacher Learning Chat

=== "Mesop"

    In this example, we'll create a simple learning [**chatbot**](https://en.wikipedia.org/wiki/Chatbot){target="_blank"} where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll use [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md) for the web interface and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) for serving and executing the workflows.

=== "Custom REST API and WebSocket"

    In this example, we'll create a simple learning [**chatbot**](https://en.wikipedia.org/wiki/Chatbot){target="_blank"} where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll create a custom client using [**HTML**](https://en.wikipedia.org/wiki/HTML){target="_blank"} and [**JavaScript**](https://en.wikipedia.org/wiki/JavaScript){target="_blank"} for the web interface and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) for serving and executing the workflows.


### Step-by-Step Breakdown

As shown in the [**architecture overview**](#architecture-overview), this setup requires **three** components (applications). Let's begin our code walkthrough, starting with the [**NATS App**](#3-nats-app).

#### 1. **Define Workflow**

To get started, define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
{! docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/workflow.py [ln:1-47] !}
```

#### 2. **Import Required Modules**

Next, import the required modules from the **FastAgency**. These imports provide the essential building blocks for integrating with the client. Additionally, import the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) class for workflow execution.

```python hl_lines="4"
{!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py [ln:1-7] !}
```

#### 3. **Configure the `NatsAdapter`**

Create an instance of the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) and pass your workflow to it. The adapter will handle the communication with the [**`NatsProvider`**](../../../api/fastagency/adapters/nats/NatsProvider.md) and distribute workflow execution to the workers.

```python hl_lines="5"
{!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py [ln:9-13] !}
```

#### 4. **Define FastAgency Application**

Create a [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) and then add it to the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} application using the [**lifespan parameter**](https://fastapi.tiangolo.com/advanced/events/){target="_blank"}.

```python
{!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py [ln:15] !}
```

#### 5. **Adapter Chaining**

Above, we created Nats.io provider that will start brokers waiting to consume initiate workflow messages from the message broker.

Next, we set up a FastAPI service to interact with the NATS.io provider. This introduces the second component: the [**FastAPI App**](#2-fastapi-app).

=== "Mesop"

    !!! note "main_2_fastapi.py"
        ```python hl_lines="15-17 19-20"
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_2_fastapi.py [ln:1-20] !}
        ```

    Finally, the last component is the [**Mesop Client App**](#1-mesop-client-app), which uses the [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md) to communicate with both the user and the [**`FastAPIProvider`**](../../../api/fastagency/adapters/fastapi/FastAPIProvider.md).

    !!! note "main_3_mesop.py"
        ```python hl_lines="7-9 11-15"
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_3_mesop.py [ln:1-15] !}
        ```

=== "Custom REST API and WebSocket"

    !!! note "main_fastapi_custom_client.py"
        ```python hl_lines="17-19 22-23"
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/main_2_fastapi_custom_client.py [ln:1-8,96-110] !}
        ```

    Finally, for simplicity, we will serve our custom HTML client as part of the same [**FastAPI App**](#2-fastapi-app) using FastAPI's [**HTMLResponse**](https://fastapi.tiangolo.com/advanced/custom-response/#html-response){target="_blank"}.

    !!! note

        - The below example uses a **simple HTML with JavaScript**, all in a single string and served directly from the FastAgency FastAPI app for **simplicity**.
        - This approach is **not suitable for production** but ideal for demonstrating core concepts.
        - In a real-world scenario, you'd use a separate frontend, built with frameworks like React or Vue.js, or other languages such as Java, Go, or Ruby, based on your project needs.

    !!! note "main_fastapi_custom_client.py"
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/main_2_fastapi_custom_client.py [ln:9-95,113-115] !}
        ```


#### 6. **Nats server setup**

The [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) requires a running NATS server. The easiest way to start the NATS server is by using [**Docker**](https://www.docker.com/){target="_blank"}. FastAgency leverages the [**JetStream**](https://docs.nats.io/nats-concepts/jetstream){target="_blank"} feature of NATS and also utilizes authentication.

```python hl_lines="1 3 8 14"
{!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/.devcontainer/nats_server.conf [ln:1-31]!}
```

In the above Nats configuration, we define a user called `fastagency`, and its password is read from the environment variable `FASTAGENCY_NATS_PASSWORD`. We also enable JetStream in Nats and configure Nats to serve via the appropriate ports.

### Complete Application Code

Please copy and paste the following code into the same folder, using the file names exactly as mentioned below.

=== "Mesop"

    <details>
        <summary>nats_server.conf</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/.devcontainer/nats_server.conf !}
        ```
    </details>

    <details>
        <summary>workflow.py</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/workflow.py !}
        ```
    </details>

    <details>
        <summary>main_1_nats.py</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py !}
        ```
    </details>

    <details>
        <summary>main_2_fastapi.py</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_2_fastapi.py !}
        ```
    </details>

    <details>
        <summary>main_3_mesop.py</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_3_mesop.py !}
        ```
    </details>

=== "Custom REST API and WebSocket"

    <details>
        <summary>nats_server.conf</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/.devcontainer/nats_server.conf !}
        ```
    </details>

    <details>
        <summary>workflow.py</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/workflow.py !}
        ```
    </details>

    <details>
        <summary>main_1_nats.py</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_nats.py !}
        ```
    </details>

    <details>
        <summary>main_2_fastapi_custom_client.py</summary>
        ```python
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/main_2_fastapi_custom_client.py !}
        ```
    </details>

### Run Application

Once everything is set up, you can run your FastAgency application using the following commands.

=== "Mesop"

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
                docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats_server.conf:/etc/nats/nats_server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats_server.conf
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
                docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats_server.conf:/etc/nats/nats_server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats_server.conf
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

=== "Custom REST API and WebSocket"

    You need to run **Three** commands in **separate** terminal windows:

    - Start **Nats** Docker container:
    !!! note "Terminal 1"
        ```
        docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats_server.conf:/etc/nats/nats_server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats_server.conf
        ```

    - Start **FastAPI** application that provides a conversational workflow:
    !!! note "Terminal 2"
        ```
        uvicorn main_1_nats:app --reload
        ```

    - Start **FastAPI** application integrated with a **Nats** messaging system:
    !!! note "Terminal 3"
        ```
        uvicorn main_2_fastapi_custom_client:app --port 8008 --reload
        ```


### Output

The outputs will vary based on the interface. Here is the output of the last terminal starting the UI:

=== "Mesop"

    ```console
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
    [2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
    ```

    ![Initial message](../../getting-started/images/chat.png)


=== "Custom REST API and WebSocket"

    ```console
    INFO:     Will watch for changes in these directories: ['/tmp/custom_fastapi_demo']
    INFO:     Uvicorn running on http://0.0.0.0:8008 (Press CTRL+C to quit)
    INFO:     Started reloader process [73937] using StatReload
    INFO:     Started server process [73940]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```
    ![Output Screenshot](../images/custom_chat_output.png)


The **FastAPI + Nats** Adapter in FastAgency provides a **highly scalable** and **flexible solution** for building distributed applications. By leveraging the power of [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} for building [**REST APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} and the [**Nats.io MQ**](https://nats.io/){target="_blank"} for asynchronous communication, you can create robust and efficient workflows that can handle high user demand and complex production setups.
