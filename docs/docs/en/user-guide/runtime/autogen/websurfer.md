# WebSurfer Tool

The `WebSurferTool` from **FastAgency** lets developers create agents that search, navigate, and gather real-time web data. It supports workflows with live browsing, automatic data retrieval, and tasks requiring current web information, making it easy to add web capabilities to your AI agents.

Let’s see how the `WebSurferTool` works with an example: “Search for information about Microsoft AutoGen and summarize the results,” highlighting its ability to browse and collect data in real time.

## Installation

Before getting started, make sure you have installed FastAgency with support for the AutoGen runtime by running the following command:

```bash
pip install "fastagency[autogen]"
```

This installation includes the AutoGen runtime, allowing you to build multi-agent workflows and integrate external APIs seamlessly.

## Example: Search for information about Microsoft AutoGen and summarize the results

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from **AutoGen** and **FastAgency**. These imports lay the foundation for building and running multi-agent workflows.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:1-9] !}
```

#### 2. **Configure the Language Model (LLM)**
Here, the large language model is configured to use the `gpt-4o` model, and the API key is retrieved from the environment. This setup ensures that both the user and websurfer agents can interact effectively.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:11-19] !}
```

#### 3. **Define the Workflow and Agents**
In this step, we create two agents:

- **UserProxyAgent**: This agent simulates the user interacting with the system.

- **ConversableAgent**: This agent serves as the websurfer and has access to the `WebSurferTool`, using it whenever real-time web data is needed.

- **WebSurferTool**: An instance of the `WebSurferTool` is registered with the caller as `ConversableAgent` and with the executor as `UserProxyAgent`. This setup allows the `ConversableAgent` to use the `WebSurferTool`, giving it the ability to perform real-time web interactions.

The workflow is registered using **[AutoGenWorkflows](../../../api/fastagency/runtime/autogen/AutoGenWorkflows/)**.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:21-51] !}
```

#### 4. **Enable Agent Interaction and Chat**
Here, the user agent starts a conversation with the websurfer agent, which performs a web search and returns summarized information. The conversation is then summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:52-59] !}
```

#### 5. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the console interface.

```python
{! docs_src/user_guide/runtime/autogen/websurfer.py [ln:62] !}
```

## Complete Application Code

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

---

This example demonstrates the power of the **AutoGen** runtime within FastAgency, showing how easy it is to integrate LLM-powered agents with real-time API services. By leveraging FastAgency, developers can quickly create interactive, scalable applications that interact with external data sources in real-time.

For more detailed documentation, visit the [AutoGen Reference](../../../api/fastagency/runtime/autogen/AutoGenWorkflows/).
