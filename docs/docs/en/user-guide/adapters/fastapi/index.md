# FastAPI

The [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) allows you to expose your FastAgency workflows as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} using the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework.

## Use Cases

When to Use the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md):

- **Custom Client Applications**: If you want to build your **own client applications** in a different language, (e.g., [**HTML**](https://en.wikipedia.org/wiki/HTML){target="_blank"}/[**JavaScript**](https://en.wikipedia.org/wiki/JavaScript){target="_blank"}, [**Go**](https://go.dev/){target="_blank"}, [**Java**](https://www.java.com/en/){target="_blank"}, etc.), that interacts with your FastAgency workflows using [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} and [**WebSockets**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"}.

- **Moderate User Demand**: This adapter is a good fit for scenarios where workflows need to be executed by [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} to efficiently handle higher machine load.

- **Simplified Production Setup**: This adapter is a good choice when you need a **simple and easy-to-manage** setup for [**deploying**](https://fastapi.tiangolo.com/deployment/){target="_blank"} FastAgency workflows as an [**ASGI**](https://asgi.readthedocs.io/en/latest/){target="_blank"} server in production.

## Architecture Overview

This section provides [**high-level architecture**](https://en.wikipedia.org/wiki/High-level_design){target="_blank"} diagrams for the two available setups of using [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} with:

- [**Mesop**](https://google.github.io/mesop/){target="_blank"} client using [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md), and

- Custom [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} and [**WebSocket**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"} client

=== "Mesop"

    ![Mesop FastAPI App](../images/mesop_fastapi.png)

    The system consists of two main components:

    #### Mesop Client App

    The client App serves as the frontend interface for the system. It includes:

    - [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md): A friendly web interface for users to interact with the workflows. It facilitates the communication with the user and the [**`FastAPIProvider`**](../../../api/fastagency/adapters/fastapi/FastAPIProvider.md).
    - [**`FastAPIProvider`**](../../../api/fastagency/adapters/fastapi/FastAPIProvider.md): A component that facilitates communication between the Mesop client and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

    This app handles all client interactions and presents the results back to the user.

    #### FastAPI App

    The FastAPI App forms the backend of our system and consists of:

    - **AutoGen Workflows**: These define the core logic and behavior of our application, utilizing agents to perform various tasks and achieve specific goals.
    - The [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md): This component communicates with [**AutoGen**](https://microsoft.github.io/autogen){target="_blank"}, and implements routes and [**websocket**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"} for [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"}.
    - [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"}: Provides the infrastructure for building and exposing [**AutoGen**](https://microsoft.github.io/autogen){target="_blank"} workflows via [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}.


=== "Custom REST API and Websocket"

    ![Custom FastAPI App](../images/custom_fastapi.png)

    The system consists of two main components:

    #### Custom Client App

    This application serves as the frontend interface for the system. It includes:

    - **Custom Client**: A client application built in a different language, (e.g., [**HTML**](https://en.wikipedia.org/wiki/HTML){target="_blank"}/[**JavaScript**](https://en.wikipedia.org/wiki/JavaScript){target="_blank"}, [**Go**](https://go.dev/){target="_blank"}, [**Java**](https://www.java.com/en/){target="_blank"}, etc.) facilitates communication between the user and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

    This application handles all interactions with the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and presents the results back to the user.

    #### FastAPI App

    The FastAPI App forms the backend of our system and consists of:

    - **AutoGen Workflows**: These define the core logic and behavior of our application, utilizing agents to perform various tasks and achieve specific goals.
    - The [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md): This component communicates with [**AutoGen**](https://microsoft.github.io/autogen){target="_blank"}, and implements routes and [**websocket**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"} for [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"}.
    - [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"}: Provides the infrastructure for building and exposing [**AutoGen**](https://microsoft.github.io/autogen){target="_blank"} workflows via [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

    #### Building Custom Client Applications

    To write a custom application that interacts with [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md), it's essential to first understand the available server routes it provides and their purposes. This knowledge forms the foundation of the [**client-server**](https://en.wikipedia.org/wiki/Client%E2%80%93server_model){target="_blank"} interaction model.

    ##### Available API Endpoints

    [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) provides three primary endpoints for building client applications:

    | Route    | Method |Purpose |
    | -------- | ------- | ------- |
    | `/fastagency/discovery`         | GET    | Lists the available workflows that can be initiated |
    | `/fastagency/initiate_workflow` | POST     | Starts a new workflow instance for the chosen workflow |
    | `/fastagency/ws`                | WebSocket    | Handles real-time workflow communication |


    Now that we understand the available routes, let's visualize how these components interact in a typical client-server communication flow.

    ##### System Interaction Flow

    The following sequence diagram illustrates the step-by-step process of how a **custom client application** interacts with the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md):

    ```mermaid
    sequenceDiagram
    participant Client as Custom Client Application
    participant FastAPI as FastAPIAdapter

    Note over Client,FastAPI: 1. Setup & Discovery Phase
    Client->>FastAPI: GET /fastagency/discovery
    FastAPI-->>Client: Available Workflows

    Client->>Client: Display workflow options to user

    Note over Client,FastAPI: 2. Workflow Initiation
    Client->>FastAPI: POST /fastagency/initiate_workflow
    FastAPI-->>Client: Workflow Configuration

    Note over Client,FastAPI: 3. WebSocket Connection
    Client->>FastAPI: Initiate a WebSocket Connection (/fastagency/ws)
    FastAPI-->>Client: WebSocket Connection Established

    Note over Client,FastAPI: 4. Real-time Communication
    Client->>FastAPI: Send Initial WebSocket Message
    FastAPI-->>Client: Acknowledge Connection

    activate FastAPI
    activate Client
    Note right of FastAPI: Message Processing Loop
    FastAPI->>Client: Send Workflow Message
    Client->>FastAPI: Send Response If Required
    FastAPI->>Client: Send Next Workflow Message
    deactivate Client
    deactivate FastAPI
    ```

    To better understand this diagram, let's break down the key steps involved in the client-server interaction:

    ##### Understanding the Flow

    The interaction between client and server follows these key steps:

    - **Discovery**: Client fetches available workflows from the server.
    - **Selection**: User selects a workflow to execute.
    - **Initiation**: Client requests to start the chosen workflow.
    - **Connection**: WebSocket connection established for real-time communication. These includes:
        - Server sending workflow message to the client.
        - Client sends optional response to server if previous server message requires user input.
        - Server processes and sends the next workflow message.


    ##### Message Types

    Before diving into the implementation, we need to learn a bit about the **message types** that [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) provides. Understanding these will help us handle messages in our custom client and display them properly to the users.

    FastAgency tags each message sent from the server to the client over [**WebSockets**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"} with a `type` attribute. This helps the client differentiate between different types of messages and handle them accordingly. Let’s break them down into two categories:

    **Messages for Display**:

    - **`text_message`**: A basic text message from the server, intended for display to the user. It doesn’t require any action from the user, serving purely as information or status updates.
    - **`workflow_started`**: This message indicates the start of a new workflow. The message includes the workflow’s name and a description along with other details.
    - **`workflow_completed`**: This message signals that the current workflow has been successfully completed. The client can use this to notify the user or transition to the next step in the application.
    - **`suggested_function_call`**: Indicates that the LLM has suggested a function call.
    - **`function_call_execution`**: Indicates that the LLM has executed the suggested function call.
    - **`error`**: Indicates that an error occurred during the workflow. The client can handle this by displaying an error message or prompting the user to retry the action.

    **Messages That Require User Response**:

    - **`text_input`**: This message prompts the client to gather input from the user. It could be a question or request for data. The client should provide a way for the user to respond (e.g., a text input or text area) and then send the response back to the server.
    - **`multiple_choice`**: This message requires the user to choose from a predefined set of options provided by the LLM. The client should present these options (e.g., checkboxes or radio buttons) and submit the user’s selection back to the server.

    A full list of message types and their detailed usage will be **available soon in the FastAgency Adapter’s OpenAPI specification**—stay tuned!

    ##### Implementation Guide

    In the following sections, we'll walk through the process of creating a custom client application that implements the flow we've just described. We'll build a simple web-based client that demonstrates how to interact with [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) effectively.

    Our implementation will cover these key aspects:

    - Fetching and displaying available workflows.
    - Handling workflow initiation.
    - Managing WebSockets connection.
    - Processing real-time messages.

    !!! note

        Before we examine the code:

        - The below example uses a **simple HTML with JavaScript**, all in a single string and served directly from the FastAPI App for **simplicity**.
        - This approach is **not suitable for production** but ideal for demonstrating core concepts.
        - In a real-world scenario, you'd use a separate frontend, built with frameworks like React or Vue.js, or other languages such as Java, Go, or Ruby, based on your project needs.

    Let's begin by looking at the code structure and then break down each component.

## Installation

We **strongly recommend** using [**Cookiecutter**](../cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**.

=== "Mesop"

    Before getting started, ensure that FastAgency is installed with support for the [**AutoGen**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime, along with the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md), **fastapi**, and **server** submodules by running the following command:

    ```bash
    pip install "fastagency[autogen,mesop,fastapi,server]"
    ```

    This command installs FastAgency with support for both the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md) and [**console**](../../../api/fastagency/ui/console/ConsoleUI.md) interfaces for [**AutoGen**](https://microsoft.github.io/autogen){target="_blank"} workflows, but with [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} serving input requests and running workflows.

=== "Custom REST API and Websocket"

    Before getting started, ensure that FastAgency is installed with support for the [**AutoGen**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime, along with the **fastapi**, and **server** submodules by running the following command:

    ```bash
    pip install "fastagency[autogen,fastapi,server]"
    ```

    This command installs FastAgency, but with [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} serving input requests and running workflows.

## Example: Student and Teacher Learning Chat

=== "Mesop"

    In this example, we'll create a simple learning [**chatbot**](https://en.wikipedia.org/wiki/Chatbot){target="_blank"} where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll use [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md) for the web interface and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to expose the workflow as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

=== "Custom REST API and Websocket"

    In this example, we'll create a simple learning [**chatbot**](https://en.wikipedia.org/wiki/Chatbot){target="_blank"} where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll create a custom client using [**HTML**](https://en.wikipedia.org/wiki/HTML){target="_blank"} and [**JavaScript**](https://en.wikipedia.org/wiki/JavaScript){target="_blank"} for the web interface and the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to expose the workflow as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

### Step-by-Step Breakdown

#### 1. **Define Workflow**

To get started, define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
{! docs_src/getting_started/fastapi/my_fastagency_app/my_fastagency_app/workflow.py [ln:1-47] !}
```

#### 2. **Import Required Modules**

=== "Mesop"

    Next, import the required modules from the **FastAgency**. Import the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) class to expose the workflows as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

    ```python hl_lines="3"
    {!> docs_src/getting_started/fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_fastapi.py [ln:1-4] !}
    ```

=== "Custom REST API and Websocket"

    Next, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating with the custom client. Additionally, import the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`HTMLResponse`**](https://fastapi.tiangolo.com/advanced/custom-response/#html-response){target="_blank"} class to expose the workflows as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

    ```python hl_lines="6 9"
    {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py [ln:1-10] !}
    ```

#### 3. **Define FastAgency Application**

Create an instance of the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and pass your workflow to it. Then, include a router to the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} application. The adapter will have all [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} and [**WebSocket**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"} routes for communicating with the client.

```python hl_lines="1 4"
{!> docs_src/getting_started/fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_fastapi.py [ln:8-11] !}
```

=== "Mesop"

    #### 4. **Adapter Chaining**

    Finally, create an additional specification file for an application using [**`MesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md) to connect to the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

    !!! note "main_2_mesop.py"
        ```python
        {!> docs_src/getting_started/fastapi/my_fastagency_app/my_fastagency_app/deployment/main_2_mesop.py [ln:1-15] !}
        ```

=== "Custom REST API and Websocket"

    #### 4. **Serving the Custom HTML Client**

    Finally, use the [**HTML Response**](https://fastapi.tiangolo.com/advanced/custom-response/#html-response){target="_blank"} from FastAPI to serve the custom client code.

    ```python
    {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py [ln:12-98,146-148] !}
    ```

### Complete Application Code

Please copy and paste the following code into the same folder, using the file names exactly as mentioned below.

=== "Mesop"

    <details>
        <summary>workflow.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/my_fastagency_app/my_fastagency_app/workflow.py !}
        ```
    </details>

    <details>
        <summary>main_1_fastapi.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/my_fastagency_app/my_fastagency_app/deployment/main_1_fastapi.py !}
        ```
    </details>

    <details>
        <summary>main_2_mesop.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/my_fastagency_app/my_fastagency_app/deployment/main_2_mesop.py !}
        ```
    </details>

=== "Custom REST API and Websocket"

    <details>
        <summary>main_fastapi_custom_client.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py !}
        ```
    </details>

### Run Application

=== "Mesop"

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

=== "Custom REST API and Websocket"

    Once everything is set up, you can run your FastAgency application using the following command.

    - Start **FastAPI** application using [**uvicorn**](https://www.uvicorn.org){target="_blank"}:
    !!! note "Terminal 1"
        ```
        uvicorn main_fastapi_custom_client:app --port 8008 --reload
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

    ![Output Screenshot](../../getting-started/images/chat.png)

=== "Custom REST API and Websocket"

    ```console
    INFO:     Will watch for changes in these directories: ['/tmp/custom_fastapi_demo']
    INFO:     Uvicorn running on http://0.0.0.0:8008 (Press CTRL+C to quit)
    INFO:     Started reloader process [73937] using StatReload
    INFO:     Started server process [73940]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```
    ![Output Screenshot](../images/custom_chat_output.png)


The [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) provides a powerful solution for developers seeking a **user-friendly** and efficient way to expose their FastAgency workflows as [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}, contributing to building production-ready applications.
