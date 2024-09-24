# WebSurfer

FastAgency allows you to quickly create workflows with capabilities like live browsing, automatic data retrieval, and tasks requiring up-to-date web information, making it easy to integrate web functionality.

## Adding Web Surfing Capabilities to Agents

FastAgency provides two ways to add web surfing capabilities to agents. You can either:

1. Use a WebSurferAgent, which comes with built-in web surfing capabilities (recommended)
2. Enhance an existing agent with web surfing capability

In this guide, we'll demonstrate both methods with a real-world example. We’ll create a workflow where agents search the web for real-time data.

We’ll build agents and assign them the task: “Search for information about Microsoft AutoGen and summarize the results” to showcase its ability to browse and gather real-time data in action.

## Installation

Before getting started, make sure you have installed FastAgency with support for the AutoGen runtime by running the following command:

```bash
pip install "fastagency[autogen]"
```

This command installs FastAgency with support for the Console interface and AutoGen framework.

## Example: Search for information about Microsoft AutoGen and summarize the results

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from **AutoGen** and **FastAgency**. These imports lay the foundation for building and running multi-agent workflows.

=== "Using WebSurferAgent"
    ```python hl_lines="7"
    {!> docs_src/user_guide/runtime/autogen/websurfer.py [ln:1-9] !}
    ```

    To create a new web surfing agent, simply import `WebSurferAgent`, which comes with built-in web surfing capabilities, and use it as needed.

=== "Enhancing an existing agent"
    ```python hl_lines="7"
    {!> docs_src/user_guide/runtime/autogen/websurfer.py [ln:1-9] !}
    ```

    For Mesop applications, import `MesopUI` to integrate with the Mesop web interface.


#### 2. **Configure the Language Model (LLM)**
Here, the large language model is configured to use the `gpt-4o` model, and the API key is retrieved from the environment. This setup ensures that both the user and websurfer agents can interact effectively.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:10-19] !}
```

#### 3. **Define the Workflow and Agents**

=== "Using WebSurferAgent"

    In this step, we are going to create two agents:

    - **UserProxyAgent**: This agent simulates the user interacting with the system.

    - **WebSurferAgent**: This agent functions as a web surfer, with built-in capability to browse the web and fetch real-time data as required.


    The workflow is registered using **[AutoGenWorkflows](../../../api/fastagency/runtime/autogen/AutoGenWorkflows.md)**.

    ```python hl_lines="18"
    {!> docs_src/user_guide/runtime/autogen/websurfer.py [ln:20-38] !}
    ```

    When initiating the `WebSurferAgent`, the executor parameter must be provided. This can be either a single instance of `ConversableAgent` or a `list of ConversableAgent` instances.

    The `WebSurferAgent` relies on the executor agent(s) to execute the web surfing tasks. In this example, the `web_surfer` agent will call the `user_proxy` agent with the necessary instructions when web surfing is required, and the `user_proxy` will execute those instructions.

=== "Enhancing an existing agent"
    ```python hl_lines="7"
    {!> docs_src/user_guide/runtime/autogen/websurfer.py [ln:1-9] !}
    ```

    In this step, we create two agents:

    - **UserProxyAgent**: This agent simulates the user interacting with the system.

    - **ConversableAgent**: This agent serves as the websurfer and has access to the `WebSurferTool`, using it whenever real-time web data is needed.

    - **WebSurferTool**: An instance of the `WebSurferTool` is registered with the caller as `ConversableAgent` and with the executor as `UserProxyAgent`. This setup allows the `ConversableAgent` to use the `WebSurferTool`, giving it the ability to perform real-time web interactions.

    The workflow is registered using **[AutoGenWorkflows](../../../api/fastagency/runtime/autogen/AutoGenWorkflows/)**.

    ```python
    {!> docs_src/user_guide/runtime/autogen/websurfer.py [ln:21-51] !}
    ```

#### 4. **Enable Agent Interaction and Chat**
Here, the user agent starts a conversation with the websurfer agent, which performs a web search and returns summarized information. The conversation is then summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:40-48] !}
```

#### 5. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the console interface.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:50] !}
```

### Complete Application Code

<details>
<summary>websurfer.py</summary>
```python
{! docs_src/user_guide/runtime/autogen/websurfer.py!}
```
</details>


### Running the Application

```bash
fastagency run websurfer.py
```

Ensure you have set your OpenAI API key in the environment. The command will launch a console interface where users can input their requests and interact with the websurfer agent.

### Output

Once you run it, FastAgency automatically detects the appropriate app to execute and runs it. The application will then prompt you with: "Please enter an initial message:".

```console
 ╭─ Python module file ─╮
 │                      │
 │  🐍 websurfer.py     │
 │                      │
 ╰──────────────────────╯

 [INFO] Importing autogen.base.py

 ╭─ Importable FastAgency app ─╮
 │                             │
 │  from websurfer import app  │
 │                             │
 ╰─────────────────────────────╯

╭─ FastAgency -> user [text_input] ────────────────────────────────────────────╮
│                                                                              │
│ Starting a new workflow 'simple_websurfer' with the following                │
│ description:                                                                 │
│                                                                              │
│ WebSurfer chat                                                               │
│                                                                              │
│ Please enter an initial message:                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

In the prompt, type **Search for information about Microsoft AutoGen and summarize the results** and press Enter.

This will initiate the task, allowing you to see the real-time conversation between the agents as they collaborate to complete it. Once the task is finished, you’ll see an output similar to the one below.

```console
╭─ workflow -> user [workflow_completed] ──────────────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "result": "Microsoft AutoGen is an open-source framework designed          │
│ to simplify the orchestration, optimization, and automation of large         │
│ language model (LLM) workflows. It features customizable agents,             │
│ multi-agent conversations, tool integration, and human involvement,          │
│ making it suitable for complex AI applications. Key resources include        │
│ the Microsoft Research Blog and the GitHub repository for AutoGen."          │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ FastAgency -> user [text_input] ────────────────────────────────────────────╮
│                                                                              │
│ Starting a new workflow 'simple_websurfer' with the following                │
│ description:                                                                 │
│                                                                              │
│ WebSurfer chat                                                               │
│                                                                              │
│ Please enter an initial message:                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

The agent will summarize its findings and then prompt you again with "Please enter an initial message:", allowing you to continue the conversation with the web surfer agent.

---

This example demonstrates the power of the AutoGen runtime within FastAgency, showcasing how easily LLM-powered agents can be integrated with browsing capabilities to fetch and process real-time information. By leveraging FastAgency, developers can quickly build interactive, scalable applications that interact with live data sources.
