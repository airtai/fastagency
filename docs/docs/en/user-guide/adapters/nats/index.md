# Nats.io

The **Nats Adapter** in FastAgency enables seamless integration of your workflows with the [**Nats.io MQ**](https://nats.io/){target="_blank"} message broker, providing a scalable and flexible solution for building distributed applications.

## Use Cases

This section outlines the scenarios where it's particularly beneficial to use the **Nats** Adapter.

### When to Use the Nats Adapter

- **Default Client Application**: If you prefer using the **default Mesop client** provided by FastAgency without the need to build your own client application.

- **High User Demand**: When your application requires **high scalability** to handle a large number of users or messages, and you are comfortable with a more complex production setup involving a message broker. For example, it's well-suited for building a **scalable chat application** for a larger company or external customers.

- **Conversation Auditing**: If you need the ability to **audit conversations**, the Nats Adapter provides the necessary infrastructure to enable this feature.

## Architecture Overview

The following diagram illustrates the high-level architecture of an application using the **Nats Adapter with Mesop UI** as its frontend:


![Mesop Nats](../images/mesop_nats.png)

The system consists of two main components:

### FastAgency Mesop App

The FastAgency Mesop App serves as the frontend interface for the system. It includes:

- **Mesop UI**: A user-friendly web interface for users to interact with the workflows. It communicates with the client and the Nats Provider.
- **Nats Provider**: The [**Nats.io MQ**](https://nats.io/){target="_blank"} message broker responsible for handling message communication between different parts of the system.

This app handles all client interactions and presents the results back to the user.

### FastAgency Nats App

The FastAgency Nats App forms the backend of the system and consists of:

- **AutoGen Workflows**: The workflows defined using the AutoGen framework. They are executed by the workers in the Nats Adapter.
- **Nats Adapter**: Communicates with AutoGen, and makes the workflow messages available on corresponding Nats topics.

### Interaction Flow

1. The client interacts with the Mesop UI to initiate a workflow.
2. The Mesop UI sends a message to the Nats Provider to initiate the workflow.
3. The Nats Adapter, connected to the Nats Provider, receives the message.
4. The Nats Adapter distributes the workflow execution task to one of the available workers.
5. The worker executes the AutoGen Workflow.
6. The results are sent back through the Nats Provider to the Mesop UI and ultimately to the client.


Now, it's time to see the Nats Adapter using FastAgency in action. Let's dive into an example and learn how to use it!

## Installation

Before getting started, make sure you have installed FastAgency by running the following command:

```bash
pip install "fastagency[autogen,mesop,fastapi,server,nats]"
```

This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows and the Nats Adapter for workflow execution.

## Example: Student and Teacher Learning Chat

In this example, we'll create a simple learning chat where a student agent asks questions and a teacher agent responds, simulating a learning environment.  We'll use MesopUI for the web interface and the Nats Adapter for workflow execution.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**

To get started, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI. Additionally, import the [**`NatsAdapter`**](../../../api/fastagency/adapters/nats/NatsAdapter.md) class for workflow execution.

```python hl_lines="9"
{!> docs_src/getting_started/nats/main_1_nats.py [ln:1-11] !}
```

#### 2. **Define Workflow**

Define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's an example workflow definition:

```python
{!> docs_src/getting_started/nats/main_1_nats.py [ln:3-57] !}
```

#### 3. **Configure the Nats Adapter**

Create an instance of the NatsAdapter and pass your workflow to it. The adapter will handle the communication with the Nats Provider and distribute workflow execution to the workers.

```python
{!> docs_src/getting_started/nats/main_1_nats.py [ln:59-64] !}
```

#### 4. **Define FastAgency Application**

Create an NatsAdapter and then add it to a FastAPI application using the lifespan parameter. The adapter will have all REST and Websocket routes for communicating with a client. For more information on the lifespan parameter, check out the official documentation [**here**](https://fastapi.tiangolo.com/advanced/events/){target="_blank"}

```python
{!> docs_src/getting_started/nats/main_1_nats.py [ln:66] !}
```

#### 5. **Nats server setup**

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

- 1. Start **Nats** Docker container:
!!! note "Terminal 1"
    ```
    docker run -d --name nats-fastagency --rm -p 4222:4222 -p 9222:9222 -p 8222:8222 -v $(pwd)/nats-server.conf:/etc/nats/nats-server.conf -e FASTAGENCY_NATS_PASSWORD='fastagency_nats_password' nats:latest -c /etc/nats/nats-server.conf
    ```

The above command starts a Nats container with the necessary ports exposed and configuration file mounted. It also sets the `FASTAGENCY_NATS_PASSWORD` environment variable for authentication.

 - 2. Start **FastAPI** application that provides a conversational workflow:
!!! note "Terminal 2"
    ```
    uvicorn main_1_nats:app --reload
    ```

This command starts the FastAPI application using Uvicorn, a lightning-fast ASGI server. The --reload flag enables auto-reloading, so any changes made to the code will be automatically reflected without needing to restart the server.

- 3. Start **Mesop** web interface using gunicorn:
!!! note "Terminal 3"
    ```
    gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
    ```

!!! danger "Currently not working on **Windows**"
    The above command is currently not working on **Windows**, because gunicorn is not supported. Please use the alternative method below to start the application:
    ```
    waitress-serve --listen=0.0.0.0:8888 main_2_mesop:app
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

The Nats Adapter in FastAgency provides a powerful and flexible way to integrate your workflows with the Nats.io message broker. By leveraging the scalability and distributed architecture of Nats, you can build highly scalable and production-ready applications. With its easy-to-use API and seamless integration with the Mesop UI, the Nats Adapter simplifies the development process while enabling advanced features like conversation auditing.
