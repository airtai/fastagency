# NATS.io

The **NATS Adapter** in FastAgency allows you to integrate your workflows with the [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker.  This interface is suitable for setups in VPN-s or, in combination with the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve public workflows in an authenticated, secure manner. To simplify such integrations, we will connect our [**NATS**](https://nats.io/){target="_blank"}-based message queue with a [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} application.

## Why Use NATS Adapter?
The NATS Adapter offers several benefits:

- **Scalability**: With the **NATS Adapter**, workflows are executed by multiple workers that connect to the [**NATS.io MQ**](https://nats.io/){target="_blank"}. These workers can run on different machines or even in different data centers or cloud providers, enabling horizontal scalability.
- **Distributed Architecture**: [**NATS.io MQ**](https://nats.io/){target="_blank"} is a distributed message broker that ensures reliable and efficient message delivery across complex, distributed environments. It allows for seamless communication between various components of your application.

## Architecture Overview

At a high level we have two FastAgency applications: the **FastAgency Mesop App** and the **FastAgency Nats App**. These applications work together to provide a seamless interface between the client and the underlying AutoGen workflows.

![Mesop Nats](../images/mesop_nats.png)

### FastAgency Mesop App

The FastAgency Mesop App serves as the front-end interface for our system. It contains:

- **Mesop UI**: Provides a web interface for users to interact with the workflows. It communicates with both the client and the NATS Provider.
- **Nats Provider**: The [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker, responsible for handling message communication between different parts of the system.

This app handles all client interactions and presents the results back to the user.

### FastAgency Nats App

The FastAgency Nats App forms the backend of our system and consists of:

- **AutoGen Workflows**: The workflows defined using the AutoGen framework. They are executed by the workers in the NATS Adapter.
- **Nats Adapter**: Responsible for connecting to the NATS Provider, receiving workflow initiation messages, and distributing them to the workers for execution.

### Interaction Flow

1. The client interacts with the Mesop UI to initiate a workflow.
2. The Mesop UI sends a message to the NATS Provider to initiate the workflow.
3. The NATS Adapter, connected to the NATS Provider, receives the message.
4. The NATS Adapter distributes the workflow execution task to one of the available workers.
5. The worker executes the AutoGen Workflow.
6. The results are sent back through the NATS Provider to the Mesop UI and ultimately to the client.


Now, it's time to see the Nats Adapter using FastAgency in action. Let's dive into an example and learn how to use it!

## Installation

Before getting started, make sure you have installed FastAgency by running the following command:

```bash
pip install "fastagency[autogen,mesop,fastapi,server,nats]"
```

This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows and the NATS Adapter for workflow execution.

## Example: Student and Teacher Learning Chat

In this example, we'll create a simple learning chat where a student agent asks questions and a teacher agent responds, simulating a learning environment.  We'll use MesopUI for the web interface and the NATS Adapter for workflow execution.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**

To get started, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI. Additionally, import the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) class for workflow execution.

```python hl_lines="9"
{!> docs_src/getting_started/nats/main_1_nats.py [ln:1-11] !}
```

#### 2. **Define Workflow**

Next, define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's an example workflow definition:

```python
{!> docs_src/getting_started/nats/main_1_nats.py [ln:3-57] !}
```

#### 3. **Configure the NATS Adapter**

Create an instance of the NatsAdapter and pass your workflow to it. The adapter will handle the communication with the NATS Provider and distribute workflow execution to the workers.

```python
{!> docs_src/getting_started/nats/main_1_nats.py [ln:59-64] !}
```

#### 4. **Define FastAgency Application**

Then, create an NatsAdapter and then add it to a FastAPI application using the lifespan parameter. The adapter will have all REST and Websocket routes for communicating with a client. For more information on the lifespan parameter, check out the official documentation [**here**](https://fastapi.tiangolo.com/advanced/events/){target="_blank"}

```python
{!> docs_src/getting_started/nats/main_1_nats.py [ln:66] !}
```

#### 5. **Nats server setup**

The `NatsAdapter` requires a running NATS server. The easiest way to start the NATS server is by using [Docker](https://www.docker.com/){target="_blank"}. FastAgency uses the [JetStream](https://docs.nats.io/nats-concepts/jetstream){target="_blank"} feature of NATS and also utilizes authentication.

```python hl_lines="1 3 6 11 17"
{!> docs_src/getting_started/nats_n_fastapi/nats-server.conf [ln:1-23]!}
```

In the above NATS configuration, we define a user called `fastagency`, and its password is read from the environment variable `FASTAGENCY_NATS_PASSWORD`. We also enable JetStream in NATS and configure NATS to serve via the appropriate ports.

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
    {!> docs_src/getting_started/nats/main_1_nats.py !}
    ```
</details>

<details>
    <summary>main_2_mesop.py</summary>
    ```python
    {!> docs_src/getting_started/nats/main_2_mesop.py !}
    ```
</details>

### Run Application

Once everything is set up, you can run your FastAgency application using the following commands. You need to run **three** commands in **separate** terminal windows:

- Start **NATS** Docker container:
!!! note "Terminal 1"
    ```
    docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats-server.conf:/etc/nats/nats-server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats-server.conf
    ```

The above command starts a NATS container with the necessary ports exposed and configuration file mounted. It also sets the `FASTAGENCY_NATS_PASSWORD` environment variable for authentication.

 - Start **FastAPI** application that provides a conversational workflow:
!!! note "Terminal 2"
    ```
    uvicorn main_1_nats:app --reload
    ```

This command starts the FastAPI application using Uvicorn, a lightning-fast ASGI server. The --reload flag enables auto-reloading, so any changes made to the code will be automatically reflected without needing to restart the server.

- Start **Mesop** web interface using gunicorn:
!!! note "Terminal 2"
    ```
    gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
    ```

This command starts the Mesop web interface using Gunicorn, a production-grade WSGI server. The -b flag specifies the binding address and port, and the --reload flag enables auto-reloading.

### Output

The outputs will vary based on the interface. Here is the output of the last terminal starting the UI:

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

![Initial message](../../../getting-started/images/chat.png)

The NATS Adapter in FastAgency provides a powerful and flexible way to integrate your workflows with the NATS.io message broker. By leveraging the scalability and distributed architecture of NATS, you can build highly scalable and production-ready applications.
