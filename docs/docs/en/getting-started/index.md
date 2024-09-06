---
# 0.5 - API
# 2 - Release
# 3 - Contributing
# 5 - Template Page
# 10 - Default
hide:
  - navigation

search:
  boost: 10
---


# Getting Started with FastAgency


<b>The fastest way to bring multi-agent workflows to production.</b>


---

<p align="center">
  <a href="https://github.com/airtai/fastagency/actions/workflows/pipeline.yaml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/pipeline.yaml/badge.svg?branch=main" alt="Test Passing"/>
  </a>

  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/airtai/fastagency" target="_blank">
      <img src="https://coverage-badge.samuelcolvin.workers.dev/airtai/fastagency.svg" alt="Coverage">
  </a>

  <a href="https://www.pepy.tech/projects/fastagency" target="_blank">
    <img src="https://static.pepy.tech/personalized-badge/fastagency?period=month&units=international_system&left_color=grey&right_color=green&left_text=downloads/month" alt="Downloads"/>
  </a>

  <a href="https://pypi.org/project/fastagency" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastagency?label=PyPI" alt="Package version">
  </a>

  <a href="https://pypi.org/project/fastagency" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastagency.svg" alt="Supported Python versions">
  </a>

  <br/>

  <a href="https://github.com/airtai/fastagency/actions/workflows/codeql.yml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/codeql.yml/badge.svg" alt="CodeQL">
  </a>

  <a href="https://github.com/airtai/fastagency/actions/workflows/dependency-review.yaml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/dependency-review.yaml/badge.svg" alt="Dependency Review">
  </a>

  <a href="https://github.com/airtai/fastagency/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/airtai/fastagency.png" alt="License">
  </a>

  <a href="https://github.com/airtai/fastagency/blob/main/CODE_OF_CONDUCT.md" target="_blank">
    <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Code of Conduct">
  </a>

  <a href="https://discord.gg/kJjSGWrknU" target="_blank">
      <img alt="Discord" src="https://img.shields.io/discord/1247409549158121512?logo=discord">
  </a>
</p>

---

Welcome to FastAgency! This guide will walk you through the initial setup and usage of FastAgency, a powerful tool that leverages the [AutoGen](https://autogen-ai.github.io/autogen/) framework to quickly build applications. FastAgency is designed to be flexible and adaptable, and we plan to extend support to additional agentic frameworks such as [CrewAI](https://www.crewai.com/) in the near future. This will provide even more options for defining workflows and integrating with various AI tools.

With FastAgency, you can create interactive applications using various interfaces such as a console or Mesop.

## Supported Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [ConsoleIO](../api/fastagency/core/io/console/ConsoleIO/) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.
- **Mesop**: Utilize [Mesop](https://google.github.io/mesop/) with [MesopIO](../api/fastagency/core/io/mesop/MesopIO/) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

We are also working on adding support for other frameworks, such as [CrewAI](https://www.crewai.com/), to broaden the scope and capabilities of FastAgency. Stay tuned for updates on these integrations.

## Install

To get started, you need to install FastAgency. You can do this using `pip`, Python's package installer. Choose the installation command based on the interface you want to use:

=== "Console"
    ```console
    pip install "fastagency[autogen]"
    ```

    This command installs FastAgency with support for the Console interface and AutoGen framework.

=== "Mesop"
    ```console
    pip install "fastagency[autogen,mesop]"
    ```

    This command installs FastAgency with support for both the Console and Mesop interfaces, providing a more comprehensive setup.

## Write Code

### Imports
Depending on the interface you choose, you'll need to import different modules. These imports set up the necessary components for your application:

=== "Console"
    ```python
    import os

    from autogen.agentchat import ConversableAgent

    from fastagency.core import Chatable
    from fastagency.core.runtimes.autogen.base import AutoGenWorkflows
    from fastagency.core.io.console import ConsoleIO

    from fastagency import FastAgency
    ```

    For Console applications, import `ConsoleIO` to handle command-line input and output.

=== "Mesop"
    ```python
    import os

    from autogen.agentchat import ConversableAgent

    from fastagency.core import Chatable
    from fastagency.core.runtimes.autogen.base import AutoGenWorkflows
    from fastagency.core.io.mesop import MesopIO

    from fastagency import FastAgency
    ```

    For Mesop applications, import `MesopIO` to integrate with the Mesop web interface.

### Define Workflow

You need to define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

wf = AutoGenWorkflows()

@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(io: Chatable, initial_message: str, session_id: str) -> str:
    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
        llm_config=llm_config,
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
        llm_config=llm_config,
    )

    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )

    return chat_result.summary
```

This code snippet sets up a simple learning chat between a student and a teacher. You define the agents and how they should interact, specifying how the conversation should be summarized.

### Define FastAgency Application

Next, define your FastAgency application. This ties together your workflow and the interface you chose:

=== "Console"
    ```python
    from fastagency.core.io.console import ConsoleIO

    app = FastAgency(wf=wf, io=ConsoleIO())
    ```

    For Console applications, use `ConsoleIO` to handle user interaction via the command line.

=== "Mesop"
    ```python
    from fastagency.core.io.mesop import MesopIO

    app = FastAgency(wf=wf, io=MesopIO())
    ```

    For Mesop applications, use `MesopIO` to enable web-based interactions.

## Run Application

Once everything is set up, you can run your FastAgency application using the following command:

```console
fastagency run
```

### Output

The output will vary based on the interface:

=== "Console"
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

    ╭─ FastAgency -> user [text_input] ────────────────────────────────────────────╮
    │                                                                              │
    │ Starting a new workflow 'simple_learning' with the following                 │
    │ description:                                                                 │
    │                                                                              │
    │ Student and teacher learning chat                                            │
    │                                                                              │
    │ Please enter an                                                              │
    │ initial message:                                                             │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

    For Console applications, you will see a command-line prompt where you can enter the initial message and interact with your workflow.

=== "Mesop"
    ```console
    ╭─ Python module file ─╮
    │                      │
    │  🐍 main_mesop.py    │
    │                      │
    ╰──────────────────────╯


    ╭─ Importable FastAgency app ──╮
    │                              │
    │  from main_mesop import app  │
    │                              │
    ╰──────────────────────────────╯

    Running with hot reload:

    Running server on: http://localhost:32123
    * Serving Flask app 'mesop.server.server'
    * Debug mode: off
    ```

    For Mesop applications, the output will include a URL where you can access your web-based application.

## Using External REST APIs

### Creating a Weather Agent

This tutorial demonstrates how to integrate external REST API calls into `AutoGen` agents using `FastAgency`. We'll create a weather agent that interacts with a weather REST API and a user agent to facilitate the conversation. This example will help you understand how to set up agents and facilitate agent communication through an external REST API. To interact with the REST API, the AutoGen agent needs to understand the available routes, so it requires the `openapi.json` file from the external REST API.

For this tutorial's use case, Airt.ai provides a [weather API](https://weather.tools.fastagency.ai/docs).

#### Install

To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```console
pip install "fastagency[autogen,openapi]"
```

#### Imports
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the `OpenAPI` Client and `UserProxyAgent`:

```python
import os

from autogen.agentchat import ConversableAgent
from autogen import UserProxyAgent

from fastagency.core import Chatable
from fastagency.core.runtimes.autogen.base import AutoGenWorkflows
from fastagency.core.io.console import ConsoleIO
from fastagency.openapi.client import Client

from fastagency import FastAgency
```

#### Define Workflow

In this workflow, the only difference is that we create a Python client for the external REST API by passing the URL of the `openapi.json` to the `Client.create` method. Then, we register the generated client with the agent using the methods `register_for_llm` and `register_for_execution`. Here's a simple example of a workflow definition:

```python
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

WEATHER_OPENAPI_URL = "https://weather.tools.fastagency.ai/openapi.json"

wf = AutoGenWorkflows()

@wf.register(name="simple_weather", description="Weather chat")
def weather_workflow(io: Chatable, initial_message: str, session_id: str) -> str:

    weather_client = Client.create(openapi_url=WEATHER_OPENAPI_URL)

    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    weather_agent = ConversableAgent(
        name="Weather_Agent",
        system_message="You are a weather agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    weather_client.register_for_llm(weather_agent)
    weather_client.register_for_execution(user_agent)

    chat_result = user_agent.initiate_chat(
        weather_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary
```

This code snippet sets up a simple weather agent that calls an external weather API using the registered functions generated from the `openapi.json` URL.

### Define FastAgency Application

Next, define your FastAgency application.

```python
from fastagency.core.io.console import ConsoleIO

app = FastAgency(wf=wf, io=ConsoleIO())
```

## Run Application

Once everything is set up, you can run your FastAgency application using the following command:

```console
fastagency run
```

### Output

The output will vary based on the city and the current weather conditions:

```console

 ╭── Python module file ──╮
 │                        │
 │  🐍 sample_weather.py  │
 │                        │
 ╰────────────────────────╯

 ╭─── Importable FastAgency app ────╮
 │                                  │
 │  from sample_weather import app  │
 │                                  │
 ╰──────────────────────────────────╯

╭─ FastAgency -> user [text_input] ────────────────────────────────────────────╮
│                                                                              │
│ Starting a new workflow 'simple_weather' with the following                  │
│ description:                                                                 │
│                                                                              │
│ Weather chat                                                                 │
│                                                                              │
│ Please enter an initial message:                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
What is the weather in Zagreb?
    ╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ What is the weather in Zagreb?                                               │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [suggested_function_call] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_weather__get",                                       │
    │   "call_id":                                                                 │
    │ "call_gGl4uAhMvPTXjgrOvkVZwCh3",                                             │
    │   "arguments": {                                                             │
    │     "city": "Zagreb"                                                         │
    │                                                                              │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ User_Agent -> Weather_Agent [function_call_execution] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_weather__get",                                       │
    │   "call_id":                                                                 │
    │ "call_gGl4uAhMvPTXjgrOvkVZwCh3",                                             │
    │   "retval": "{\"city\": \"Zagreb\",                                          │
    │ \"temperature\": 18, \"daily_forecasts\": [{\"forecast_date\":               │
    │ \"2024-09-06\", \"temperature\": 23, \"hourly_forecasts\":                   │
    │ [{\"forecast_time\": \"00:00:00\", \"temperature\": 19,                      │
    │ \"description\": \"Patchy rain nearby\"}, {\"forecast_time\":                │
    │ \"03:00:00\", \"temperature\": 19, \"description\": \"Patchy light           │
    │ drizzle\"}, {\"forecast_time\": \"06:00:00\", \"temperature\": 18,           │
    │ \"description\": \"Clear\"}, {\"forecast_time\": \"09:00:00\",               │
    │ \"temperature\": 24, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"12:00:00\", \"temperature\": 30, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"15:00:00\", \"temperature\": 30,                       │
    │ \"description\": \"Partly Cloudy\"}, {\"forecast_time\": \"18:00:00\",       │
    │  \"temperature\": 26, \"description\": \"Patchy rain nearby\"},              │
    │ {\"forecast_time\": \"21:00:00\", \"temperature\": 21,                       │
    │ \"description\": \"Patchy rain nearby\"}]}, {\"forecast_date\":              │
    │ \"2024-09-07\", \"temperature\": 24, \"hourly_forecasts\":                   │
    │ [{\"forecast_time\": \"00:00:00\", \"temperature\": 19,                      │
    │ \"description\": \"Partly Cloudy\"}, {\"forecast_time\": \"03:00:00\",       │
    │  \"temperature\": 18, \"description\": \"Clear\"}, {\"forecast_time\":       │
    │  \"06:00:00\", \"temperature\": 18, \"description\": \"Clear\"},             │
    │ {\"forecast_time\": \"09:00:00\", \"temperature\": 25,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"12:00:00\",               │
    │ \"temperature\": 30, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"15:00:00\", \"temperature\": 31, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"18:00:00\", \"temperature\": 26,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"21:00:00\",               │
    │ \"temperature\": 22, \"description\": \"Clear\"}]},                          │
    │ {\"forecast_date\": \"2024-09-08\", \"temperature\": 25,                     │
    │ \"hourly_forecasts\": [{\"forecast_time\": \"00:00:00\",                     │
    │ \"temperature\": 20, \"description\": \"Partly Cloudy\"},                    │
    │ {\"forecast_time\": \"03:00:00\", \"temperature\": 19,                       │
    │ \"description\": \"Clear\"}, {\"forecast_time\": \"06:00:00\",               │
    │ \"temperature\": 18, \"description\": \"Clear\"}, {\"forecast_time\":        │
    │ \"09:00:00\", \"temperature\": 26, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"12:00:00\", \"temperature\": 31,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"15:00:00\",               │
    │ \"temperature\": 32, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"18:00:00\", \"temperature\": 27, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"21:00:00\", \"temperature\": 23,                       │
    │ \"description\": \"Partly Cloudy\"}]}]}\n"                                   │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ The current weather in Zagreb is 18°C. Here are the upcoming weather         │
    │ forecasts:                                                                   │
    │                                                                              │
    │ ### September 6, 2024                                                        │
    │ - **Day Temperature**: 23°C                                                  │
    │ -                                                                            │
    │ **Hourly Forecast**:                                                         │
    │   - 00:00: 19°C - Patchy rain nearby                                         │
    │   - 03:00:                                                                   │
    │ 19°C - Patchy light drizzle                                                  │
    │   - 06:00: 18°C - Clear                                                      │
    │   - 09:00: 24°C -                                                            │
    │ Sunny                                                                        │
    │   - 12:00: 30°C - Sunny                                                      │
    │   - 15:00: 30°C - Partly Cloudy                                              │
    │   -                                                                          │
    │ 18:00: 26°C - Patchy rain nearby                                             │
    │   - 21:00: 21°C - Patchy rain nearby                                         │
    │                                                                              │
    │                                                                              │
    │ ### September 7, 2024                                                        │
    │ - **Day Temperature**: 24°C                                                  │
    │ - **Hourly                                                                   │
    │ Forecast**:                                                                  │
    │   - 00:00: 19°C - Partly Cloudy                                              │
    │   - 03:00: 18°C - Clear                                                      │
    │                                                                              │
    │ - 06:00: 18°C - Clear                                                        │
    │   - 09:00: 25°C - Sunny                                                      │
    │   - 12:00: 30°C - Sunny                                                      │
    │                                                                              │
    │   - 15:00: 31°C - Sunny                                                      │
    │   - 18:00: 26°C - Sunny                                                      │
    │   - 21:00: 22°C -                                                            │
    │ Clear                                                                        │
    │                                                                              │
    │ ### September 8, 2024                                                        │
    │ - **Day Temperature**: 25°C                                                  │
    │ - **Hourly                                                                   │
    │ Forecast**:                                                                  │
    │   - 00:00: 20°C - Partly Cloudy                                              │
    │   - 03:00: 19°C - Clear                                                      │
    │                                                                              │
    │ - 06:00: 18°C - Clear                                                        │
    │   - 09:00: 26°C - Sunny                                                      │
    │   - 12:00: 31°C - Sunny                                                      │
    │                                                                              │
    │   - 15:00: 32°C - Sunny                                                      │
    │   - 18:00: 27°C - Sunny                                                      │
    │   - 21:00: 23°C -                                                            │
    │ Partly Cloudy                                                                │
    │                                                                              │
    │ If you need more information, feel free to ask!                              │
    ╰──────────────────────────────────────────────────────────────────────────────╯
```

## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, such as [CrewAI](https://www.crewai.com/), to provide more flexibility and options for building applications. This will allow you to define workflows using a variety of frameworks and leverage their unique features and functionalities.

Feel free to customize your workflow and application based on your needs. For more details on configurations and additional features, refer to the [AutoGen documentation](https://autogen-ai.github.io/autogen/) and [Mesop documentation](https://google.github.io/mesop/).

---

## Stay in touch

Please show your support and stay in touch by:

- giving our [GitHub repository](https://github.com/airtai/fastagency/) a star, and

- joining our [Discord server](https://discord.gg/kJjSGWrknU)

Your support helps us to stay in touch with you and encourages us to
continue developing and improving the framework. Thank you for your
support!

---

## Contributors

Thanks to all of these amazing people who made the project better!

<a href="https://github.com/airtai/fastagency/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=airtai/fastagency"/>
</a>
