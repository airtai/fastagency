# AutoGen in FastAgency

The **AutoGen** runtime is a key component of FastAgency, empowering developers to create intelligent, multi-agent systems powered by large language models (LLMs). AutoGen allows agents to communicate, collaborate, and perform complex tasks autonomously while easily integrating with external APIs for real-time data and functionality.

In this example, we will create a simple weather chatbot using **AutoGen** in FastAgency. The chatbot will enable a user to interact with a weather agent that fetches real-time weather information from an external API using OpenAPI specifications.

## Installation

Before getting started, make sure you have installed FastAgency with support for the AutoGen runtime by running the following command:

```bash
pip install "fastagency[autogen]"
```

This installation includes the AutoGen runtime, allowing you to build multi-agent workflows and integrate external APIs seamlessly.

## Example: Integrating a Weather API with AutoGen

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from **AutoGen** and **FastAgency**. These imports lay the foundation for building and running multi-agent workflows.

```python
{! docs_src/user_guide/runtime/autogen/main.py [ln:1-11] !}
```

#### 2. **Configure the Language Model (LLM)**
Here, the large language model is configured to use the `gpt-4o` model, and the API key is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/runtime/autogen/main.py [ln:12-22] !}
```

#### 3. **Set Up the Weather API**
We define the OpenAPI specification URL for the weather service. This API will later be used by the weather agent to fetch real-time weather data.

```python
{! docs_src/user_guide/runtime/autogen/main.py [ln:23-26] !}
```

#### 4. **Define the Workflow and Agents**
In this step, we create two agents:

- **UserProxyAgent**: This agent simulates the user interacting with the system.

- **ConversableAgent**: This agent acts as the weather agent, responsible for fetching weather data from the API.

The workflow is registered using **[AutoGenWorkflows](../../../api/fastagency/runtime/autogen/AutoGenWorkflows/)**.

```python
{! docs_src/user_guide/runtime/autogen/main.py [ln:27-45] !}
```

#### 5. **Register API Functions with the Agents**
In this step, we register the weather API functions to ensure that the weather agent can call the correct functions, such as `get_daily_weather` and `get_daily_weather_weekly_get`, to retrieve the required weather data.

```python
{! docs_src/user_guide/runtime/autogen/main.py [ln:46-60] !}
```

#### 6. **Enable Agent Interaction and Chat**
Here, the user agent initiates a chat with the weather agent, which queries the API and returns the weather information. The conversation is summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/runtime/autogen/main.py [ln:61-69] !}
```

#### 7. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the console interface.

```python
{! docs_src/user_guide/runtime/autogen/main.py [ln:71-72] !}
```

### Running the Application

```bash
cd docs/docs_src/user_guide/runtime/autogen
fastagency run main.py
```

Ensure you have set your OpenAI API key in the environment and that the weather API URL is accessible. The command will launch a console interface where users can input their requests and interact with the weather agent.

---

This example demonstrates the power of the **AutoGen** runtime within FastAgency, showing how easy it is to integrate LLM-powered agents with real-time API services. By leveraging FastAgency, developers can quickly create interactive, scalable applications that interact with external data sources in real-time.

For more detailed documentation, visit the [AutoGen Reference](../../../api/fastagency/runtime/autogen/AutoGenWorkflows/).
