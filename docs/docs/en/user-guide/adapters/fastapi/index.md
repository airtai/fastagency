# FastAPI

The **FastAPI Adapter** in FastAgency allows you to expose your workflows as a REST API using the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework.

## Why Use FastAPI Adapter?

The FastAPI Adapter provides several benefits:

- **Scalability**: FastAPI supports execution with **multiple workers**, allowing you to scale your workflows horizontally. Each workflow is executed in the context of a **WebSocket connection**, enabling efficient handling of concurrent requests.
- **API-driven Development**: By exposing your workflows as a **REST API**, you can easily integrate them with other systems and services. This enables you to build robust and scalable applications that leverage the power of agentic workflows.

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

To scale your FastAgency application using the FastAPI Adapter, you can leverage the multi-worker support provided by FastAPI. By running multiple instances of your application behind a load balancer, you can distribute the incoming requests across multiple workers.

For example, you can use a process manager like Gunicorn to run multiple worker processes:
```cmd
gunicorn main_1_fastapi:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

This command starts Gunicorn with 4 worker processes, each running an instance of your FastAPI application. The incoming requests will be distributed among these workers, allowing for efficient handling of concurrent requests.
