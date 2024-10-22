# FastAPI

The **FastAPI Adapter** allows you to expose your FastAgency workflows as a REST API using the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework.

## Use Cases

This section outlines the scenarios where it's particularly beneficial to use the **FastAPI** Adapter.

### When to Use the FastAPI Adapter

- **Custom Client Applications**: If you want to build your **own client applications** that interact with your FastAgency workflows using REST APIs, this adapter provides greater flexibility and control over the client-side implementation.
- **Moderate User Demand**: The FastAPI Adapter is a good fit for scenarios with **moderate user request volume**. For example, it's well-suited for a medium-sized company developing an internal custom chat application.
- **Simplified Production Setup**: Choose this adapter if you need a **simple and easy-to-manage** production setup for deploying your FastAgency workflows as a REST API.


## Architecture Overview

The following section presents high-level architecture diagrams for the two available setups:

- **FastAPI with Mesop Client**
- **FastAPI with Custom Client**

=== "FastAPI with Mesop Client"

    ![Mesop FastAPI App](../images/mesop_fastapi.png)

    The system consists of two main components:

    #### FastAgency Client App

    The FastAgency Client App serves as the frontend interface for the system. It includes:

    - **Mesop Client**: A friendly web interface for users to interact with the workflows. It facilitates the communication with the user and the FastAPI Provider.
    - **FastAPI Provider**: A component that facilitates communication between the Mesop client and the FastAPI Adapter.

    This app handles all client interactions and presents the results back to the user.

    #### FastAgency FastAPI App

    The FastAgency FastAPI App forms the backend of our system and consists of:

    - **AutoGen Workflows**: These define the core logic and behavior of our application, utilizing agents to perform various tasks and achieve specific goals.
    - **FastAPI Adapter**: This component communicates with AutoGen, and implements routes and websocket for FastAPI.
    - **FastAPI**: Provides the infrastructure for building and exposing AutoGen workflows via REST API.

    #### Interaction Flow

    1. The user initiates communication with the Mesop client in the FastAgency Client App.
    2. The Mesop client interacts with the FastAPI Provider, sending requests based on user actions.
    3. The FastAPI Provider communicates these requests to the FastAPI Adapter in the FastAgency FastAPI App.
    4. The FastAPI Adapter processes the requests and triggers the appropriate AutoGen workflows.
    5. The AutoGen workflows execute, performing the required tasks and generating results.
    6. Results are sent back through the FastAPI Adapter to the FastAPI Provider.
    7. The FastAPI Provider relays the results to the Mesop client, which then presents them to the user.

=== "FastAPI with Custom Client"

    ![Custom FastAPI App](../images/custom_fastapi.png)

    The system consists of two main components:

    #### FastAgency Client App

    The FastAgency Client App serves as the frontend interface for the system. It includes:

    - **Custom Client**: A custom web interface for users to interact with the workflows. It facilitates the communication with the user and the **FastAgency FastAPI App**.

    This custom client app handles all interactions with the **FastAgency FastAPI App** and presents the results back to the user.

    #### FastAgency FastAPI App

    The FastAgency FastAPI App forms the backend of our system and consists of:

    - **AutoGen Workflows**: These define the core logic and behavior of our application, utilizing agents to perform various tasks and achieve specific goals.
    - **FastAPI Adapter**: This component communicates with AutoGen, and implements routes and websocket for FastAPI.
    - **FastAPI**: Provides the infrastructure for building and exposing AutoGen workflows via REST API.

    #### Building Custom Client Applications

    To write a custom application that interacts with FastAgency FastAPI App, we first need to understand the **available server routes** and their purposes. This knowledge forms the foundation of our client-server interaction model.

    ##### Available API Endpoints

    FastAgency FastAPI App provides three primary endpoints for building client applications:

    | Route    | Method |Purpose |
    | -------- | ------- | ------- |
    | `/fastagency/discovery`         | GET    | Lists the available workflows that can be initiated |
    | `/fastagency/initiate_workflow` | POST     | Starts a new workflow instance for the chosen workflow |
    | `/fastagency/ws`                | WebSocket    | Handles real-time workflow communication |


    Now that we understand the available routes, let's visualize how these components interact in a typical client-server communication flow.

    ##### System Interaction Flow

    The following sequence diagram illustrates the step-by-step process of how a **custom client application** interacts with the FastAgency FastAPI server:

    ```mermaid
    sequenceDiagram
    participant Client as Custom Client Application
    participant FastAPI as FastAgency FastAPI App

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
        - Server sending workflow message to the client
        - Client sends optional response to server if previous server message requires user input
        - Server processes and sends the next workflow message


    #### Message Types

    Before diving into the implementation, we need to learn a bit about the **message types** that FastAgency FastAPI adapter provides. Understanding these will help us handle messages in our custom client and display them properly to the users.

    FastAgency tags each message sent from the server to the client over WebSocket with a `type` attribute. This helps the client differentiate between different types of messages and handle them accordingly. Let’s break them down into two categories:

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

    #### Implementation Guide

    In the following sections, we'll walk through the process of creating a custom client application that implements the flow we've just described. We'll build a simple web-based client that demonstrates how to interact with **FastAgency FastAPI App** effectively.

    Our implementation will cover these key aspects:

    - Fetching and displaying available workflows
    - Handling workflow initiation
    - Managing WebSocket connections
    - Processing real-time messages

    !!! note

        Before we examine the code:

        - The below example uses a **simple HTML with JavaScript**, all in a single string and served directly from the FastAgency FastAPI app for **simplicity**.
        - This approach is **not suitable for production** but ideal for demonstrating core concepts.
        - In a real-world scenario, you'd use a separate frontend, built with frameworks like React or Vue.js, or other languages such as Java, Go, or Ruby, based on your project needs.

    Let's begin by looking at the code structure and then break down each component.

## Installation

Before getting started, make sure you have installed FastAgency by running the following command:

=== "FastAPI with Mesop Client"

    ```bash
    pip install "fastagency[autogen,mesop,fastapi,server]"
    ```

    This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, but with FastAPI serving input requests and running workflows.

=== "FastAPI with Custom Client"

    ```bash
    pip install "fastagency[autogen,fastapi,server]"
    ```

    This command installs FastAgency, but with FastAPI serving input requests and running workflows.

## Example: Student and Teacher Learning Chat

=== "FastAPI with Mesop Client"

    In this example, we'll create a simple learning chat where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll use MesopUI for the web interface and the FastAPI Adapter to expose the workflow as a REST API.

=== "FastAPI with Custom Client"

    In this example, we'll create a simple learning chat where a student agent asks questions and a teacher agent responds, simulating a learning environment. We'll create a custom client for the web interface and the FastAPI Adapter to expose the workflow as a REST API.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**

=== "FastAPI with Mesop Client"

    To get started, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI. Additionally, import the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) class to expose the workflows as a REST API.

    ```python hl_lines="8"
    {!> docs_src/getting_started/fastapi/main_1_fastapi.py [ln:1-9] !}
    ```

=== "FastAPI with Custom Client"

    To get started, import the required modules from the **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating with the Custom client. Additionally, import the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`HTMLResponse`**](https://fastapi.tiangolo.com/advanced/custom-response/#html-response){target="_blank"} class to expose the workflows as a REST API.

    ```python hl_lines="6 9"
    {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py [ln:1-10] !}
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

=== "FastAPI with Mesop Client"

    #### 4. **Adapter Chaining**

    Finally, create an additional specification file for an application using **MesopUI** to connect to the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

    !!! note "main_2_mesop.py"
        ```python
        {!> docs_src/getting_started/fastapi/main_2_mesop.py [ln:1-11] !}
        ```

=== "FastAPI with Custom Client"

    #### 4. **Serving the Custom HTML Client**

    Finally, use the HTML Response from FastAPI to serve the custom client code.

    ```python
    {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py [ln:12-98,146-148] !}
    ```

### Complete Application Code

Please copy and paste the following code into the same folder, using the file names exactly as mentioned below.

=== "FastAPI with Mesop Client"

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

=== "FastAPI with Custom Client"

    <details>
        <summary>main_fastapi_custom_client.py</summary>
        ```python
        {!> docs_src/getting_started/fastapi/main_fastapi_custom_client.py !}
        ```
    </details>

### Run Application

=== "FastAPI with Mesop Client"

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

    !!! danger "Currently not working on **Windows**"
        The above command is currently not working on **Windows**, because gunicorn is not supported. Please use the alternative method below to start the application:
        ```
        waitress-serve --listen=0.0.0.0:8888 main_2_mesop:app
        ```

=== "FastAPI with Custom Client"

    Once everything is set up, you can run your FastAgency application using the following command.

    - Start **FastAPI** application using uvicorn:
    !!! note "Terminal 1"
        ```
        uvicorn main_fastapi_custom_client:app --host 0.0.0.0 --port 8008 --reload
        ```

### Output

The outputs will vary based on the interface. Here is the output of the last terminal starting the UI:

=== "FastAPI with Mesop Client"

    ```console
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
    [2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
    ```

    ![Output Screenshot](../../../getting-started/images/chat.png)

=== "FastAPI with Custom Client"

    ```console
    INFO:     Will watch for changes in these directories: ['/tmp/custom_fastapi_demo']
    INFO:     Uvicorn running on http://0.0.0.0:8008 (Press CTRL+C to quit)
    INFO:     Started reloader process [73937] using StatReload
    INFO:     Started server process [73940]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```
    ![Output Screenshot](../images/custom_chat_output.png)


The **FastAPI Adapter** provides a powerful solution for developers seeking a **user-friendly** and efficient way to expose their FastAgency workflows as **REST APIs**, contributing to building production-ready applications.
