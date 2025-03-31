# WebSurfer

FastAgency allows you to quickly create workflows with capabilities like live browsing, automatic data retrieval, and tasks requiring up-to-date web information, making it easy to integrate web functionality.

## Adding Web Surfing Capabilities to Agents

FastAgency provides two ways to add web surfing capabilities to agents. You can either:

1. Use a WebSurferAgent, which comes with built-in web surfing capabilities (recommended)
2. Enhance an existing agent with web surfing capability

In this guide, we'll demonstrate both methods with a real-world example. We’ll create a workflow where agents search the web for real-time data.

We’ll build agents and assign them the task: “Search for information about AG2 (formerly AutoGen) and summarize the results” to showcase its ability to browse and gather real-time data in action.

## Installation & Setup

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**. Before getting started, make sure you have installed FastAgency with support for the AG2 runtime by running the following command:

```bash
pip install "fastagency[autogen]"
```

This command installs FastAgency with support for the Console interface and AG2 framework.

### Create Bing Web Search API Key
To create [Bing Web Search](https://www.microsoft.com/en-us/bing/apis/pricing){target="_blank"} API key, follow the guide provided.

!!! note
    You will need to create **Microsoft Azure** Account.

#### Set Up Your API Key in the Environment

You can set the Binga API key in your terminal as an environment variable:

=== "Linux/macOS"
    ```bash
    export BING_API_KEY="your_bing_api_key"
    ```
=== "Windows"
    ```bash
    set BING_API_KEY="your_bing_api_key"
    ```

## Example: Search for information about AG2 (formerly AutoGen) and summarize the results

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from **AG2** and **FastAgency**. These imports lay the foundation for building and running multi-agent workflows.

=== "Using WebSurferAgent"
    ```python hl_lines="8"
    {!> docs_src/user_guide/runtimes/autogen/websurfer.py [ln:1-9] !}
    ```

    To create a new web surfing agent, simply import `WebSurferAgent`, which comes with built-in web surfing capabilities, and use it as needed.

=== "Enhancing an existing agent"
    ```python hl_lines="4 9"
    {!> docs_src/user_guide/runtimes/autogen/websurfer_tool.py [ln:1-10] !}
    ```

    To enhance existing agents with web surfing capability, import `WebSurferTool` from FastAgency and `ConversableAgent` from AG2.


#### 2. **Configure the Language Model (LLM)**
Here, the large language model is configured to use the `gpt-4o` model, and the API key is retrieved from the environment. This setup ensures that both the user and websurfer agents can interact effectively.

```python
{! docs_src/user_guide/runtimes/autogen/websurfer.py [ln:10-19] !}
```

#### 3. **Define the Workflow and Agents**

=== "Using WebSurferAgent"

    In this step, we are going to create two agents and specify the initial message that will be displayed to users when the workflow starts:

    - **UserProxyAgent**: This agent simulates the user interacting with the system.

    - **WebSurferAgent**: This agent functions as a web surfer, with built-in capability to browse the web and fetch real-time data as required.

    ```python hl_lines="18-25"
    {!> docs_src/user_guide/runtimes/autogen/websurfer.py [ln:20-45] !}
    ```

    When initiating the `WebSurferAgent`, the executor parameter must be provided. This can be either a single instance of `ConversableAgent` or a `list of ConversableAgent` instances.

    The `WebSurferAgent` relies on the executor agent(s) to execute the web surfing tasks. In this example, the `web_surfer` agent will call the `user_agent` agent with the necessary instructions when web surfing is required, and the `user_agent` will execute those instructions.

=== "Enhancing an existing agent"

    In this step, we create two agents, a web surfer tool and set an initial message that will be displayed to users when the workflow starts:

    - **UserProxyAgent**: This agent simulates the user interacting with the system.

    - **ConversableAgent**: This is the conversable agent to which we will be adding web surfing capabilities.

    - **WebSurferTool**: The tool that gives the ConversableAgent the ability to browse the web after it has been registered.

    ```python hl_lines="27-32"
    {!> docs_src/user_guide/runtimes/autogen/websurfer_tool.py [ln:21-53] !}
    ```

    Now, we need to register the WebSurferAgent with a caller and executor. This setup allows the caller to use the WebSurferAgent for performing real-time web interactions.

    ```python  hl_lines="2 3"
    {!> docs_src/user_guide/runtimes/autogen/websurfer_tool.py [ln:54-58] !}
    ```

    The `executor` can be either a single instance of `ConversableAgent` or a `list of ConversableAgent` instances.

    The `caller` relies on the executor agent(s) to execute the web surfing tasks. In this example, the `assistant_agent` agent will call the `user_agent` agent with the necessary instructions when web surfing is required, and the `user_agent` will execute those instructions.

#### 4. **Enable Agent Interaction and Chat**
Here, the user agent starts a conversation with the websurfer agent, which performs a web search and returns summarized information. The conversation is then summarized using a method provided by the LLM.

=== "Using WebSurferAgent"

    ```python
    {! docs_src/user_guide/runtimes/autogen/websurfer.py [ln:46-53] !}
    ```

=== "Enhancing an existing agent"

    ```python
    {! docs_src/user_guide/runtimes/autogen/websurfer_tool.py [ln:59-68] !}
    ```

#### 5. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the console interface.

```python
{! docs_src/user_guide/runtimes/autogen/websurfer.py [ln:57] !}
```

### Complete Application Code

=== "Using WebSurferAgent"

    <details>
        <summary>websurfer_agent.py</summary>
        ```python
        {!> docs_src/user_guide/runtimes/autogen/websurfer.py !}
        ```
    </details>

=== "Enhancing an existing agent"

    <details>
        <summary>websurfer_tool.py</summary>
        ```python
        {!> docs_src/user_guide/runtimes/autogen/websurfer_tool.py !}
        ```
    </details>


### Running the Application


=== "Using WebSurferAgent"

    ```bash
    fastagency run websurfer_agent.py
    ```

=== "Enhancing an existing agent"

    ```bash
    fastagency run websurfer_tool.py
    ```

Ensure you have set your OpenAI API key in the environment. The command will launch a console interface where users can input their requests and interact with the websurfer agent.

### Output

Once you run it, FastAgency automatically detects the appropriate app to execute and runs it. The application will then prompt you with: "I can help you with your web search. What would you like to know?:"

=== "Using WebSurferAgent"

    ```console
    ╭── Python module file ───╮
    │                         │
    │  🐍 websurfer_agent.py  │
    │                         │
    ╰─────────────────────────╯

    [INFO] Importing autogen.base.py
    [INFO] Initializing FastAgency <FastAgency title=FastAgency application> with workflows: <fastagency.runtimes.autogen.  autogen.AutoGenWorkflows object at 0x109a51610> and UI: <fastagency.ui.console.console.ConsoleUI object at 0x109adced0>
    [INFO] Initialized FastAgency: <FastAgency title=FastAgency application>

    ╭──── Importable FastAgency app ────╮
    │                                   │
    │  from websurfer_agent import app  │
    │                                   │
    ╰───────────────────────────────────╯

    ╭─ FastAgency -> user [workflow_started] ──────────────────────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "name": "simple_websurfer",                                                │
    │   "description": "WebSurfer chat",                                           │
    │                                                                              │
    │ "params": {}                                                                 │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you with your web search. What would you like to know?:           │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

=== "Enhancing an existing agent"

    ```console
    ╭── Python module file ──╮
    │                        │
    │  🐍 websurfer_tool.py  │
    │                        │
    ╰────────────────────────╯

    [INFO] Importing autogen.base.py
    [INFO] Initializing FastAgency <FastAgency title=FastAgency application> with workflows: <fastagency.runtimes.autogen.autogen.AutoGenWorkflows object at 0x11368cbd0> and UI: <fastagency.ui.console.console.ConsoleUI object at 0x13441c510>
    [INFO] Initialized FastAgency: <FastAgency title=FastAgency application>

    ╭─── Importable FastAgency app ────╮
    │                                  │
    │  from websurfer_tool import app  │
    │                                  │
    ╰──────────────────────────────────╯

    ╭─ FastAgency -> user [workflow_started] ──────────────────────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "name": "simple_websurfer",                                                │
    │   "description": "WebSurfer chat",                                           │
    │                                                                              │
    │ "params": {}                                                                 │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you with your web search. What would you like to know?:           │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```


In the prompt, type **Search for information about AG2 (formerly AutoGen) and summarize the results** and press Enter.

This will initiate the task, allowing you to see the real-time conversation between the agents as they collaborate to complete it. Once the task is finished, you’ll see an output similar to the one below.

```console
╭─ workflow -> user [workflow_completed] ──────────────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "result": "AG2 (formerly AutoGen) is an open-source framework designed          │
│ to simplify the orchestration, optimization, and automation of large         │
│ language model (LLM) workflows. It features customizable agents,             │
│ multi-agent conversations, tool integration, and human involvement,          │
│ making it suitable for complex AI applications. Key resources include        │
│ the Microsoft Research Blog and the GitHub repository for AG2."          │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ FastAgency -> user [workflow_started] ──────────────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "name": "simple_websurfer",                                                │
│   "description": "WebSurfer chat",                                           │
│                                                                              │
│ "params": {}                                                                 │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you with your web search. What would you like to know?:           │
    ╰──────────────────────────────────────────────────────────────────────────────╯

```

The agent will summarize its findings and then prompt you again with "I can help you with your web search. What would you like to know?:", allowing you to continue the conversation with the web surfer agent.

---

This example demonstrates the power of the AG2 runtime within FastAgency, showcasing how easily LLM-powered agents can be integrated with browsing capabilities to fetch and process real-time information. By leveraging FastAgency, developers can quickly build interactive, scalable applications that interact with live data sources.
