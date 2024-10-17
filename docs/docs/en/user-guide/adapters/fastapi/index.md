# FastAPI

The **FastAPI Adapter** allows you to expose your FastAgency workflows as a REST API using the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework.

## Use Cases

This section outlines the scenarios where it's particularly beneficial to use the FastAPI Adapter.

### When to Use the FastAPI Adapter:

- **Custom Client Applications**: Use this adapter when you want to build your own client application that interacts with your FastAgency workflows using the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework.
- **Moderate User Demand**: The FastAPI Adapter is a good fit for scenarios with moderate user request volume. For example, it's well-suited for a medium-sized company developing an internal custom chat application.
- **Simplified Production Setup**: Choose this adapter if you need a simple and easy-to-manage production setup for deploying your FastAgency workflows as a REST API.


## Architecture Overview

Here's a high-level overview of an application using the **FastAPI Adapter with Mesop UI** as its frontend:

![Mesop FastAPI](../images/mesop_fastapi.png)

The system consists of two main components:


### FastAgency Mesop App

The FastAgency Mesop App serves as the front-end interface for our system. It contains:

- **Mesop UI**: A web-based user interface that allows clients to interact with the application.
- **FastAPI Provider**: A component that facilitates communication between the Mesop UI and the FastAPI Adapter.

This app handles all client interactions and presents the results back to the user.

### FastAgency FastAPI App

The FastAgency FastAPI App forms the backend of our system and consists of:

- **AutoGen Workflows**: These define the core logic and behavior of our application, utilizing agents to perform various tasks and achieve specific goals.
- **FastAPI Adapter**: This component receives requests from the FastAPI Provider and executes the corresponding AutoGen workflows.
- **FastAPI**: The framework that provides the infrastructure for building and exposing our autogen workflows via REST API.

### Interaction Flow

1. The client initiates communication with the Mesop UI in the FastAgency Mesop App.
2. The Mesop UI interacts with the FastAPI Provider, sending requests based on user actions.
3. The FastAPI Provider communicates these requests to the FastAPI Adapter in the FastAgency FastAPI App.
4. The FastAPI Adapter processes the requests and triggers the appropriate AutoGen workflows.
5. The AutoGen workflows execute, performing the required tasks and generating results.
6. Results are sent back through the FastAPI Adapter to the FastAPI Provider.
7. The FastAPI Provider relays the results to the Mesop UI, which then presents them to the client.

This architecture ensures a clear separation between the user interface and the core application logic, allowing for flexibility in development and maintenance. The use of FastAPI provides a robust and efficient API layer, while the AutoGen workflows enable complex, agent-based task execution.

Now, it's time to see the FastAPI Adapter using FastAgency in action. Let's dive into an example and learn how to use it!

## Installation

Before getting started, make sure you have installed FastAgency by running the following command:

```bash
pip install "fastagency[autogen,mesop,fastapi,server]"
```

This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, but with FastAPI serving input requests and running workflows.

## Example: Student and Teacher Learning Chat

In this example, we'll create a simple learning chat where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll use MesopUI for the web interface and the FastAPI Adapter to expose the workflow as a REST API.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**

To get started, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI. Additionally, import the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) class to expose the workflows as a REST API.

```python hl_lines="8"
{!> docs_src/getting_started/fastapi/main_1_fastapi.py [ln:1-9] !}
```

#### 2. **Define Workflow**

Next, define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
{! docs_src/getting_started/main_console.py [ln:9-53] !}
```

#### 3. **Define FastAgency Application**

Create an instance of the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and pass your workflow to it. Then, include a router to the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} application. The adapter will have all REST API and WebSocket routes for communicating with the client.

```python hl_lines="1 4"
{!> docs_src/getting_started/fastapi/main_1_fastapi.py [ln:55-58] !}
```

#### 4. **Adapter Chaining**

Finally, create an additional specification file for an application using **MesopUI** to connect to the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

!!! note "main_2_mesop.py"
    ```python hl_lines="7-9 11"
    {!> docs_src/getting_started/fastapi/main_2_mesop.py [ln:1-11] !}
    ```



### Complete Application Code

Please copy and paste the following code into the same folder, using the file names exactly as mentioned below.

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

### Run Application

Once everything is set up, you can run your FastAgency application using the following commands. You need to run **two** commands in **separate** terminal windows:

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

### Output

The outputs will vary based on the interface. Here is the output of the last terminal starting the UI:

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

![Initial message](../../../getting-started/images/chat.png)

## Scaling with FastAPI Adapter

FastAPI's multi-worker support enables you to enhance the scalability of your FastAgency application using the FastAPI Adapter. This example illustrates how to achieve this by launching Gunicorn with four worker processes:

```cmd
gunicorn main_1_fastapi:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

In this configuration, each of the four worker processes runs an independent instance of your FastAPI application. Gunicorn effectively manages these workers, distributing incoming requests among them. This approach leads to more efficient handling of concurrent requests, ultimately improving the application's ability to manage increased traffic.
