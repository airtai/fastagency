# AutoGen in FastAgency

The **AutoGen** runtime is a key component of FastAgency, empowering developers to create intelligent, multi-agent systems powered by large language models (LLMs). AutoGen allows agents to communicate, collaborate, and perform complex tasks autonomously while easily integrating with external APIs for real-time data and functionality.

In this example, we will create a simple weather chatbot using **AutoGen** in FastAgency. The chatbot will enable a user to interact with a weather agent that fetches real-time weather information from an external API using OpenAPI specifications.

## Installation

Before getting started, make sure you have installed FastAgency with support for the AutoGen runtime by running the following command:

```bash
pip install "fastagency[autogen,openapi]"
```

This installation includes the AutoGen runtime, allowing you to build multi-agent workflows and integrate external APIs seamlessly.

## Example: Integrating a Weather API with AutoGen

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from **AutoGen** and **FastAgency**. These imports lay the foundation for building and running multi-agent workflows.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:1-10] !}
```

#### 2. **Configure the Language Model (LLM)**
Here, the large language model is configured to use the `gpt-4o` model, and the API key is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:12-20] !}
```

#### 3. **Set Up the Weather API**
We define the OpenAPI specification URL for the weather service. This API will later be used by the weather agent to fetch real-time weather data.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:22-24] !}
```

#### 4. **Define the Workflow and Agents**
In this step, we define two agents and specify the initial message that will be displayed to users when the workflow starts.

- **UserProxyAgent**: This agent simulates the user interacting with the system.

- **ConversableAgent**: This agent acts as the weather agent, responsible for fetching weather data from the API.

The workflow is registered using **[AutoGenWorkflows](../../../api/fastagency/runtimes/autogen/AutoGenWorkflows/)**.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:26-51] !}
```

#### 5. **Register API Functions with the Agents**
In this step, we register the weather API functions to ensure that the weather agent can call the correct functions, such as `get_daily_weather` and `get_daily_weather_weekly_get`, to retrieve the required weather data.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:52-65] !}
```

#### 6. **Enable Agent Interaction and Chat**
Here, the user agent initiates a chat with the weather agent, which queries the API and returns the weather information. The conversation is summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:67-74] !}
```

#### 7. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the console interface.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:77] !}
```

### Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/runtimes/autogen/main.py!}
```
</details>


### Running the Application

```bash
fastagency run
```

Ensure you have set your OpenAI API key in the environment and that the weather API URL is accessible. The command will launch a console interface where users can input their requests and interact with the weather agent.

### Output

Once you run it, FastAgency automatically detects the appropriate app to execute and runs it. The application will then prompt you with: "I can help you with the weather. What would you like to know?".

```console
╭─ Python module file ─╮
│                      │
│  🐍 main.py          │
│                      │
╰──────────────────────╯


╭─ Importable FastAgency app ─╮
│                             │
│  from main import app       │
│                             │
╰─────────────────────────────╯

╭─ FastAgency -> user [workflow_started] ──────────────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "name": "simple_weather",                                                  │
│   "description": "Weather chat",                                             │
│                                                                              │
│ "params": {}                                                                 │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
│                                                                              │
│ I can help you with the weather. What would you like to know?:               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

This example demonstrates the power of the **AutoGen** runtime within FastAgency, showing how easy it is to integrate LLM-powered agents with real-time API services. By leveraging FastAgency, developers can quickly create interactive, scalable applications that interact with external data sources in real-time.

For more detailed documentation, visit the [AutoGen Reference](../../../api/fastagency/runtimes/autogen/AutoGenWorkflows/).
