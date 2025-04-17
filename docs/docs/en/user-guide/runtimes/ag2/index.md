# AG2 in FastAgency

The [**AG2**](../../../api/fastagency/runtimes/ag2/ag2/Workflow.md) runtime is a key component of FastAgency, empowering developers to create intelligent, [**multi-agent systems**](https://docs.ag2.ai/latest/docs/user-guide/basic-concepts/orchestration/orchestrations/){target="_blank"} powered by [**large language models (LLMs)**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"}. It allows agents to communicate, collaborate, and perform complex tasks autonomously while easily integrating with external [**Rest APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} for real-time data and functionality.

In this example, we will create a simple weather [**chatbot**](https://en.wikipedia.org/wiki/Chatbot){target="_blank"} using [**AG2**](../../../api/fastagency/runtimes/ag2/ag2/Workflow.md) runtime in FastAgency. The chatbot will enable a user to interact with a weather agent that fetches real-time weather information from an external REST API using [**OpenAPI specification**](https://en.wikipedia.org/wiki/OpenAPI_Specification){target="_blank"}.

## Installation

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**. Before getting started, make sure you have installed FastAgency with support for the [**AG2**](../../../api/fastagency/runtimes/ag2/ag2/Workflow.md) runtime along with the [**mesop**](../../../api/fastagency/ui/mesop/MesopUI.md) and [**openapi**](../../../api/fastagency/api/openapi/OpenAPI.md) submodules by running the following command:

```bash
pip install "fastagency[autogen,mesop,openapi]"
```

These components enable you to build  [**multi-agent workflows**](https://docs.ag2.ai/latest/docs/user-guide/basic-concepts/orchestration/orchestrations/){target="_blank"} and seamlessly integrate with the external [**Rest APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"}.

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

## Example: Integrating a Weather API with AG2

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from [**AG2**](https://docs.ag2.ai/){target="_blank"} and **FastAgency**. These imports lay the foundation for building and running [**multi-agent**](https://docs.ag2.ai/latest/docs/user-guide/basic-concepts/orchestration/orchestrations/){target="_blank"} workflows.

```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py [ln:1-10] !}
```

#### 2. **Configure the Language Model (LLM)**
Here, the [**large language model**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"} is configured to use the Open AI's [**`gpt-4o-mini`**](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/){target="_blank"} model, and the [**API key**](https://en.wikipedia.org/wiki/API_key){target="_blank"} is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py [ln:12-16] !}
```

#### 3. **Set Up the Weather API**
We define the [**OpenAPI specification**](https://en.wikipedia.org/wiki/OpenAPI_Specification){target="_blank"} URL for the weather service. This [**Rest APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} will later be used by the weather agent to fetch real-time weather data.

```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py [ln:18-20] !}
```

#### 4. **Define the Workflow and Agents**
In this step, we define two agents and specify the initial message that will be displayed to users when the workflow starts.

- [**`UserProxyAgent`**](https://docs.ag2.ai/latest/docs/api-reference/autogen/UserProxyAgent/){target="_blank"}: This agent simulates the user interacting with the system.

- [**`ConversableAgent`**](https://docs.ag2.ai/latest/docs/api-reference/autogen/ConversableAgent/#conversableagent){target="_blank"}: This agent acts as the weather agent, responsible for fetching weather data from the API.

The workflow is registered using **[Workflow](../../../api/fastagency/runtimes/ag2/Workflow.md)**.

```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py [ln:28-52] !}
```

#### 5. **Register API Functions with the Agents**
In this step, we register the [**weather API**](https://weather.tools.fastagency.ai/docs){target="_blank"} functions to ensure that the weather agent can call the correct functions, such as `get_daily_weather` and `get_daily_weather_weekly_get`, to retrieve the required weather data.

```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py [ln:54-67] !}
```

#### 6. **Enable Agent Interaction and Chat**
Here, the user agent initiates a chat with the weather agent, which queries the [**weather API**](https://weather.tools.fastagency.ai/docs){target="_blank"} and returns the weather information. The conversation is summarized using a method provided by the [**LLM**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"}.

```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py [ln:69-76] !}
```

#### 7. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the [**`mesop`**](../../../api/fastagency/ui/mesop/MesopUI.md) interface.

```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py [ln:79] !}
```

### Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/runtimes/ag2/mesop/main.py!}
```
</details>


### Running the Application

The preferred way to run the [**Mesop**](https://google.github.io/mesop/){target="_blank"} application is using a Python WSGI HTTP server like [**Gunicorn**](https://gunicorn.org/){target="_blank"} on Linux and Mac or [**Waitress**](https://docs.pylonsproject.org/projects/waitress/en/stable/){target="_blank"} on Windows.

=== "Cookiecutter"
    !!! note "Terminal"
        ```console
        gunicorn main:app
        ```
=== "env + pip"

    First, install the package using package manager such as `pip` and then run it:

    === "Linux/MacOS"
        !!! note "Terminal"
            ```console
            pip install gunicorn
            gunicorn main:app
            ```

    === "Windows"
        !!! note "Terminal"
            ```console
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

This example demonstrates the power of the [**AG2**](../../../api/fastagency/runtimes/ag2/ag2/Workflow.md) runtime within FastAgency, showing how easy it is to integrate [**LLM**](https://en.wikipedia.org/wiki/Large_language_model){target="_blank"}-powered agents with real-time [**Rest API**](https://en.wikipedia.org/wiki/REST){target="_blank"} services. By leveraging FastAgency, developers can quickly create interactive, scalable applications that interact with external data sources in real-time.

For more detailed documentation, visit the [**AG2 Reference**](../../../api/fastagency/runtimes/ag2/Workflow.md).
