# FastAPI + Nats.io

The **FastAPI + Nats.io** Adapter in FastAgency offers the most scalable setup by combining the power of the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework for building and exposing workflows as [**REST APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} with the [**Nats.io MQ**](https://nats.io/){target="_blank"} message broker for **scalable and asynchronous** communication. This setup is the **preferred way** for running large workloads in production.

## Use Cases

This section outlines the scenarios where it's particularly beneficial to use the **FastAPI + Nats** Adapter.

### When to Use the FastAPI + Nats.io Adapter

- **Custom Client Applications**: If you want to build your **own client applications** that interact with your FastAgency workflows using REST APIs, this adapter provides greater flexibility and control over the client-side implementation.
- **High User Demand**: When your application needs to handle a large number of users or messages and requires high scalability, the FastAPI + Nats Adapter is an excellent choice. It is well-suited for building **scalable custom chat applications for larger companies or external customers**.
- **Conversation Auditing**: If you need the ability to **audit conversations**, the Nats Adapter provides the necessary infrastructure to enable this feature.


## Architecture Overview

The following section presents high-level architecture diagrams for the two available setups:

- **FastAPI + Nats Adapter with Mesop Client**
- **FastAPI + Nats Adapter with Custom Client**

=== "FastAPI + Nats Adapter with Mesop Client"

    ![Mesop FastAPI](../images/mesop_fastapi_nats.png)

    The system is composed of three main components:

    #### FastAgency Client App

    The FastAgency Client App serves as the frontend interface for the system. It includes:

    - **Mesop Client**: A friendly web interface for users to interact with the workflows. It facilitates the communication with the user and the FastAPI Provider.
    - **FastAPI Provider**: A component that facilitates communication between the Mesop client and the FastAPI Adapter.

    This app handles all client interactions and presents the results back to the user.

    #### FastAgency FastAPI App

    The FastAgency FastAPI App forms the backend of our system and consists of:

    - **Nats Provider**: Responsible for connecting to the Nats Provider, receiving workflow initiation messages, and distributing them to the workers for execution.
    - **FastAPI Adapter**: This component communicates with AutoGen, and implements routes and websocket for FastAPI.
    - **FastAPI**: Provides the infrastructure for building and exposing AutoGen workflows via REST API.

    #### FastAgency Nats App
    - **Nats Adapter**: This adapter connects to the Nats Provider. Its primary responsibility is to receive workflow initiation messages and delegate them to available workers for execution.
    - **AutoGen Workflows**: These workflows, defined using the AutoGen framework, embody the core logic and behavior of your application. They leverage agents to perform various tasks and accomplish specific goals.

    #### Interaction Flow
    1. The user initiates communication with the Mesop client in the FastAgency Client App.
    2. The Mesop client relays requests, based on user actions, to the FastAPI Provider.
    3. The FastAPI Provider forwards these requests to the FastAPI Adapter in the FastAgency FastAPI App.
    4. The FastAPI Adapter processes the requests and sends a message to the Nats Provider to start the workflow.
    5. The Nats Adapter, connected to the Nats Provider, receives the workflow initiation message.
    6. The Nats Adapter distributes the task of executing the workflow to one of the available workers.
    7. The designated worker executes the AutoGen Workflow and sends the results back through the Nats Provider to the FastAPI Adapter.
    8. The FastAPI Adapter sends the results to the FastAPI Provider, which relays them to the Mesop client for presentation to the client.

    This architecture promotes a clear separation of concerns between the user interface, the API layer, and the workflow execution logic, enhancing modularity and maintainability. The FastAPI framework provides a user-friendly and efficient API, while the Nats Adapter, coupled with the Nats.io MQ message broker, ensures scalability and asynchronous communication.

=== "FastAPI + Nats Adapter with Custom Client"

    ![Mesop FastAPI](../images/custom_fastapi_nats.png)

    The system is composed of three main components:

    #### FastAgency Client App

    The FastAgency Client App serves as the frontend interface for the system. It includes:

    - **Custom Client**: A custom web interface for users to interact with the workflows. It facilitates the communication with the user and the **FastAgency FastAPI App**.

    This custom client app handles all interactions with the **FastAgency FastAPI App** and presents the results back to the user.

    #### FastAgency FastAPI App

    The FastAgency FastAPI App forms the backend of our system and consists of:

    - **Nats Provider**: Responsible for connecting to the Nats Provider, receiving workflow initiation messages, and distributing them to the workers for execution.
    - **FastAPI Adapter**: This component communicates with AutoGen, and implements routes and websocket for FastAPI.
    - **FastAPI**: Provides the infrastructure for building and exposing AutoGen workflows via REST API.

    #### FastAgency Nats App
    - **Nats Adapter**: This adapter connects to the Nats Provider. Its primary responsibility is to receive workflow initiation messages and delegate them to available workers for execution.
    - **AutoGen Workflows**: These workflows, defined using the AutoGen framework, embody the core logic and behavior of your application. They leverage agents to perform various tasks and accomplish specific goals.

    #### Building Custom Client Applications

    For details on building a custom client that interacts with the FastAgency FastAPI backend, check out the guide [here](../fastapi/index.md#building-custom-client-applications). It covers the routes, message types, and integration steps in detail, helping you set up seamless communication with FastAgency’s FastAPI backend.

Now, it's time to see the **FastAPI + Nats Adapter** using FastAgency in action. Let's dive into an example and learn how to use it!

## Installation

Before getting started, make sure you have installed FastAgency by running the following command:

=== "FastAPI + Nats Adapter with Mesop Client"

    ```bash
    pip install "fastagency[autogen,mesop,fastapi,server,nats]"
    ```

    This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, but with FastAPI serving input requests and independent workers communicating over Nats.io protocol running workflows.

=== "FastAPI + Nats Adapter with Custom Client"

    ```bash
    pip install "fastagency[autogen,fastapi,server,nats]"
    ```

    This command installs FastAgency, but with FastAPI serving input requests and independent workers communicating over Nats.io protocol running workflows.

## Example: Student and Teacher Learning Chat

=== "FastAPI + Nats Adapter with Mesop Client"

    In this example, we'll create a simple learning chat where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll use **MesopUI** for the web interface and the **FastAPI + Nats** Adapter to expose the workflow as a REST API.

=== "FastAPI + Nats Adapter with Custom Client"

    In this example, we'll create a simple learning chat where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll create a custom client for the web interface and the FastAPI Adapter to expose the workflow as a REST API.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**

=== "FastAPI + Nats Adapter with Mesop Client"

    To get started, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI.Additionally, import the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) class for workflow execution.

    ```python hl_lines="8"
    {!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py [ln:1-9] !}
    ```

=== "FastAPI + Nats Adapter with Custom Client"

    To get started, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating with the Custom client. Additionally, import the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`HTMLResponse`**](https://fastapi.tiangolo.com/advanced/custom-response/#html-response){target="_blank"} class to expose the workflows as a REST API.

    ```python hl_lines="6 9"
    {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py [ln:1-10] !}
    ```

#### 2. **Define Workflow**

Next, define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
{! docs_src/getting_started/main_console.py [ln:9-53] !}
```

#### 3. **Configure the Nats Adapter**

Create an instance of the NatsAdapter and pass your workflow to it. The adapter will handle the communication with the Nats Provider and distribute workflow execution to the workers.

```python hl_lines="5 7"
{!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py [ln:55-60] !}
```

#### 4. **Define FastAgency Application**

Create an NatsAdapter and then add it to a FastAPI application using the lifespan parameter. The adapter will have all REST and Websocket routes for communicating with a client. For more information on the lifespan parameter, check out the official documentation [**here**](https://fastapi.tiangolo.com/advanced/events/){target="_blank"}

```python
{!> docs_src/getting_started/nats_n_fastapi/main_1_nats.py [ln:61] !}
```

#### 5. **Adapter Chaining**

Above, we created Nats.io provider that will start brokers waiting to consume initiate workflow messages from the message broker. Now, we create FastAPI service interacting with Nats.io provider:

!!! note "main_2_fastapi.py"
    ```python hl_lines="16-18 21-22"
    {!> docs_src/getting_started/nats_n_fastapi/main_2_fastapi.py [ln:1-22] !}
    ```

=== "FastAPI + Nats Adapter with Mesop Client"
    Finally, we create Mesop app communicating with the FastAPI application:

    !!! note "main_3_mesop.py"
        ```python hl_lines="7-9 11"
        {!> docs_src/getting_started/nats_n_fastapi/main_3_mesop.py [ln:1-11] !}
        ```

=== "FastAPI + Nats Adapter with Custom Client"

    Finally, use the HTML Response from FastAPI to serve the custom client code.

    ```python
    {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py [ln:12-98,146-148] !}
    ```

#### 6. **Nats server setup**

The `NatsAdapter` requires a running Nats server. The easiest way to start the Nats server is by using [Docker](https://www.docker.com/){target="_blank"}. FastAgency uses the [JetStream](https://docs.nats.io/nats-concepts/jetstream){target="_blank"} feature of Nats and also utilizes authentication.

```python hl_lines="1 3 6 11 17"
{!> docs_src/getting_started/nats_n_fastapi/nats-server.conf [ln:1-23]!}
```

In the above Nats configuration, we define a user called `fastagency`, and its password is read from the environment variable `FASTAGENCY_NATS_PASSWORD`. We also enable JetStream in Nats and configure Nats to serve via the appropriate ports.

### Complete Application Code

Please copy and paste the following code into the same folder, using the file names exactly as mentioned below.

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

Once everything is set up, you can run your FastAgency application using the following commands. You need to run **Four** commands in **separate** terminal windows:

- Start **Nats** Docker container:
!!! note "Terminal 1"
    ```
    docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats-server.conf:/etc/nats/nats-server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats-server.conf
    ```

- Start **FastAPI** application that provides a conversational workflow:
!!! note "Terminal 2"
    ```
    uvicorn main_1_nats:app --reload
    ```

- Start **FastAPI** application integrated with a **Nats** messaging system:
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
    waitress-serve --listen=0.0.0.0:8888 main_3_mesop:app
    ```

### Output

The outputs will vary based on the interface. Here is the output of the last terminal starting the UI:

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

![Initial message](../../../getting-started/images/chat.png)

The **FastAPI + Nats** Adapter in FastAgency provides a **highly scalable** and **flexible solution** for building distributed applications. By leveraging the power of [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} for building REST APIs and the [**Nats.io MQ**](https://nats.io/){target="_blank"} for asynchronous communication, you can create robust and efficient workflows that can handle high user demand and complex production setups.

Whether you're building custom client applications, scalable chat systems, or applications that require conversation auditing, the FastAPI + Nats Adapter has you covered.
