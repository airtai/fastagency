# AutoGen in FastAgency

The [**autogen**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime is a key component of FastAgency, empowering developers to create intelligent, [**multi-agent systems**](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat){target="_blank"} powered by [**large language models (LLMs)**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"}. It allows agents to communicate, collaborate, and perform complex tasks autonomously while easily integrating with external [**Rest APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} for real-time data and functionality.

In this example, we will create a simple weather [**chatbot**](https://en.wikipedia.org/wiki/Chatbot){target="_blank"} using [**autogen**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime in FastAgency. The chatbot will enable a user to interact with a weather agent that fetches real-time weather information from an external REST API using [**OpenAPI specification**](https://en.wikipedia.org/wiki/OpenAPI_Specification){target="_blank"}.

## Installation

Before you get started, ensure that you have FastAgency installed. Run the following command:

```bash
pip install "fastagency[autogen,mesop,openapi]"
```

This command installs the FastAgency library along with the  [**autogen**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime and the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md) and [**openapi**](../../../api/fastagency/api/openapi/OpenAPI.md) submodules. These components enable you to build  [**multi-agent workflows**](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat){target="_blank"} and seamlessly integrate with the external [**Rest APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

## Prerequisites

Before you begin this guide, ensure you have:

- **OpenAI account and API Key**: This guide uses OpenAI's [**`gpt-4o-mini`**](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/){target="_blank"} model, so you'll need access to it. Follow the steps in the section below to create your [**OpenAI**](https://openai.com){target="_blank"} account and obtain your API key.

### Setting Up Your OpenAI Account and API Key

**1. Create a OpenAI account:**

- Go to <b><a href="https://platform.openai.com/signup" target="_blank">https://platform.openai.com/signup</a></b>.
- Choose a **sign-up** option and follow the instructions to create your account.
- If you already have an account, simply **log-in**.

**2. Obtain your API Key:**

- Go to <b><a href="https://platform.openai.com/account/api-keys" target="_blank">https://platform.openai.com/account/api-keys</a></b>.
- Click **Create new secret key** button.
- In the popup, provide a **Name** for the key, then click **Create secret key** button.
- The key will be shown on the screen—click **Copy** button, and you're ready to go!

#### Set Up Your API Keys in the Environment

To securely use the API keys in your project, you should store it as an [**environment variable**](https://en.wikipedia.org/wiki/Environment_variable){target="_blank"}.

Run the following command in the [**same terminal**](#running-the-application) where you will run the FastAgency application. This environment variable must be set for the application to function correctly; **skipping this step will cause the example application to crash**.

=== "Linux/macOS"
    ```bash
    export OPENAI_API_KEY="your_open_api_key"
    ```
=== "Windows"
    ```bash
    set OPENAI_API_KEY="your_open_api_key"
    ```

## Example: Integrating a Weather API with AutoGen

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from [**AutoGen**](https://microsoft.github.io/autogen/){target="_blank"} and **FastAgency**. These imports lay the foundation for building and running [**multi-agent**](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat){target="_blank"} workflows.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:1-10] !}
```

#### 2. **Configure the Language Model (LLM)**
Here, the [**large language model**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"} is configured to use the Open AI's [**`gpt-4o-mini`**](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/){target="_blank"} model, and the [**API key**](https://en.wikipedia.org/wiki/API_key){target="_blank"} is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:12-20] !}
```

#### 3. **Set Up the Weather API**
We define the [**OpenAPI specification**](https://en.wikipedia.org/wiki/OpenAPI_Specification){target="_blank"} URL for the weather service. This [**Rest APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} will later be used by the weather agent to fetch real-time weather data.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:22-24] !}
```

#### 4. **Define the Workflow and Agents**
In this step, we define two agents and specify the initial message that will be displayed to users when the workflow starts.

- [**`UserProxyAgent`**](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/user_proxy_agent/#userproxyagent){target="_blank"}: This agent simulates the user interacting with the system.

- [**`ConversableAgent`**](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/#conversableagent){target="_blank"}: This agent acts as the weather agent, responsible for fetching weather data from the API.

The workflow is registered using **[AutoGenWorkflows](../../../api/fastagency/runtimes/autogen/AutoGenWorkflows/)**.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:32-56] !}
```

#### 5. **Register API Functions with the Agents**
In this step, we register the [**weather API**](https://weather.tools.fastagency.ai/docs){target="_blank"} functions to ensure that the weather agent can call the correct functions, such as `get_daily_weather` and `get_daily_weather_weekly_get`, to retrieve the required weather data.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:58-72] !}
```

#### 6. **Enable Agent Interaction and Chat**
Here, the user agent initiates a chat with the weather agent, which queries the [**weather API**](https://weather.tools.fastagency.ai/docs){target="_blank"} and returns the weather information. The conversation is summarized using a method provided by the [**LLM**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"}.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:73-81] !}
```

#### 7. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the [**`mesop`**](../../../api/fastagency/ui/mesop/MesopUI.md) interface.

```python
{! docs_src/user_guide/runtimes/autogen/main.py [ln:83] !}
```

### Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/runtimes/autogen/main.py!}
```
</details>


### Running the Application

!!! note

    In this example, AutoGen will utilize its [**code execution**](https://microsoft.github.io/autogen/0.2/docs/tutorial/code-executors#use-code-execution-in-conversation){target="_blank"} feature to execute external [**Rest APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} and retrieve their responses. For security reasons, AutoGen defaults to running code execution inside a [**Docker**](https://www.docker.com/){target="_blank"} container. If Docker is not running on the machine where you are executing this example, you will encounter the following error:

    ```cmd
    [INFO] Workflow 'simple_weather' completed with result: Unhandled exception occurred
    when executing the workflow: Code execution is set to be run in docker (default behaviour)
    but docker is not running.

    The options available are:
        - Make sure docker is running (advised approach for code execution)
        - Set "use_docker": False in code_execution_config
        - Set AUTOGEN_USE_DOCKER to "0/False/no" in your environment variables
    ```

    For more details on this and running code execution locally without Docker, follow this guide: [**Run code execution locally**](https://microsoft.github.io/autogen/blog/2024/01/23/Code-execution-in-docker/#run-code-execution-locally){target="_blank"}.

There are two options of running a Mesop application:

1. Using [**`fastagency`**](../../cli/index.md) command line:

    !!! note "Terminal (using [**`fastagency`**](../../cli/index.md))"
        ```
        fastagency run
        ```

    !!! danger "Currently not working on **MacOS**"
        The above command is currently not working on **MacOS**, please use the alternative way of starting the application from below ([#362](https://github.com/airtai/fastagency/issues/362){target="_blank"}).

2. Using [**Gunicorn**](https://gunicorn.org/){target="_blank"} WSGI HTTP server:

    The preferred way to run the [**Mesop**](https://google.github.io/mesop/){target="_blank"} application is using a Python WSGI HTTP server like [**Gunicorn**](https://gunicorn.org/){target="_blank"}. First, you need to install it using package manager such as `pip` and then run it as follows:

    !!! note "Terminal (using [**Gunicorn**](https://gunicorn.org/){target="_blank"})"
        ```
        pip install gunicorn
        gunicorn main:app
        ```

    !!! danger "Currently not working on **Windows**"
        The above command is currently not working on **Windows**, because gunicorn is not supported. Please use the alternative method below to start the application:
        ```
        pip install waitress
        waitress-serve --listen=0.0.0.0:8000 main:app
        ```

Ensure you have set your [**OpenAI API key**](https://platform.openai.com/api-keys){target="_blank"} in the environment and that the [**weather API**](https://weather.tools.fastagency.ai/docs){target="_blank"} URL is accessible. The command will launch a [**`mesopUI`**](../../../api/fastagency/ui/mesop/MesopUI.md) interface where users can input their requests and interact with the weather agent.

### Output

Once you run the command above, FastAgency will start a [**Mesop**](https://google.github.io/mesop/){target="_blank"} application. Below is the output from the terminal along with a partial screenshot of the Mesop application:

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8000 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

![Initial message](./images/weather_chat.png)

---

This example demonstrates the power of the [**autogen**](../../../api/fastagency/runtimes/autogen/autogen/AutoGenWorkflows.md) runtime within FastAgency, showing how easy it is to integrate [**LLM**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"}-powered agents with real-time [**Rest API**](https://en.wikipedia.org/wiki/REST){target="_blank"} services. By leveraging FastAgency, developers can quickly create interactive, scalable applications that interact with external data sources in real-time.

For more detailed documentation, visit the [AutoGen Reference](../../../api/fastagency/runtimes/autogen/AutoGenWorkflows/).
