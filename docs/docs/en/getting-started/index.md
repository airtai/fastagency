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

## Function Calling

In this tutorial, we will demonstrate how to implement function calling using `FastAgency` and `AutoGenWorkflows` to create an interactive chatbot experience between a student and teacher. This tutorial will cover creating LLM-powered agents, registering functions to simulate chat-based workflows, and defining the `FastAgency` application.


### Defining LLM Functions

This section describes how to define functions for the `ConversableAgent` instances representing the student and teacher. We will also explain the differences between `MultipleChoice`, `SystemMessage`, and `TextInput`, which are used for communication between the user and agents.

Let's define three functions which will be avaliable to the agents:

**Retrieving Exam Questions**

This function allows the student to request exam questions from the teacher and provides some suggestions using `TextInput`. `TextInput` is suitable for free-form text messages, ideal for open-ended queries and dialogues.
```python
def retrieve_exam_questions(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = TextInput(
            sender="student",
            recepient="teacher",
            prompt=message,
            suggestions=["1) Mona Lisa", "2) Innovations", "3) Florence at the time of Leonardo", "4) The Last Supper", "5) Vitruvian Man"],
        )
        return io.process_message(msg)
    except Exception as e:
        return f"retrieve_exam_questions() FAILED! {e}"
```

**Writing Final Answers**

This function logs the final answers after the student completes the discussion using `SystemMessage` to log the event. `SystemMessage` is used for operational or system-related instructions, such as logging data, and is not part of the agent dialogue.

```python
def write_final_answers(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = SystemMessage(
            sender="function call logger",
            recepient="system",
            message={
                "operation": "storing final answers",
                "content": message,
            },
        )
        io.process_message(msg)
        return "Final answers stored."
    except Exception as e:
        return f"write_final_answers() FAILED! {e}"
```

**Getting the Final Grade**

This function retrieves the final grade for the student's submitted answers using `MultipleChoice`, presenting the user with grading options. `MultipleChoice` is used for structured responses where the user must select one of several predefined options.

```python
def get_final_grade(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = MultipleChoice(
            sender="student",
            recepient="teacher",
            prompt=message,
            choices=["A", "B", "C", "D", "F"],
        )
        return io.process_message(msg)
    except Exception as e:
        return f"get_final_grade() FAILED! {e}"
```

### Registering LLM Functions
We now register these functions with the workflow, linking the `student_agent` as the caller and the `teacher_agent` as the executor.

```python
register_function(
    retrieve_exam_questions,
    caller=student_agent,
    executor=teacher_agent,
    name="retrieve_exam_questions",
    description="Get exam questions from examiner",
)

register_function(
    write_final_answers,
    caller=student_agent,
    executor=teacher_agent,
    name="write_final_answers",
    description="Write final answers to exam questions.",
)

register_function(
    get_final_grade,
    caller=student_agent,
    executor=teacher_agent,
    name="get_final_grade",
    description="Get the final grade after submitting answers.",
)
```

### Define FastAgency Application
Finally, we'll define the entire application:

```python
import os
from typing import Annotated

from autogen.agentchat import ConversableAgent
from autogen import register_function

from fastagency.core import Chatable
from fastagency.core.runtimes.autogen.base import AutoGenWorkflows

from fastagency.core.base import MultipleChoice, SystemMessage, TextInput

from fastagency import FastAgency


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


@wf.register(name="exam_practice", description="Student and teacher chat")
def exam_learning(io: Chatable, initial_message: str, session_id: str) -> str:

    def is_termination_msg(msg: str) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student writing a practice test. Your task is as follows:\n"
            "  1) Retrieve exam questions by calling a function.\n"
            "  2) Write a draft of proposed answers and engage in dialogue with your tutor.\n"
            "  3) Once you are done with the dialogue, register the final answers by calling a function.\n"
            "  4) Retrieve the final grade by calling a function.\n"
            "Finally, terminate the chat by saying 'TERMINATE'.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a teacher.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    def retrieve_exam_questions(message: Annotated[str, "Message for examiner"]) -> str:
        try:
            msg = TextInput(
                sender="student",
                recepient="teacher",
                prompt=message,
                suggestions=["1) Mona Lisa", "2) Innovations", "3) Florence at the time of Leonardo", "4) The Last Supper", "5) Vitruvian Man"],
            )
            return io.process_message(msg)
        except Exception as e:
            return f"retrieve_exam_questions() FAILED! {e}"

    def write_final_answers(message: Annotated[str, "Message for examiner"]) -> str:
        try:
            msg = SystemMessage(
                sender="function call logger",
                recepient="system",
                message={
                    "operation": "storing final answers",
                    "content": message,
                },
            )
            io.process_message(msg)
            return "Final answers stored."
        except Exception as e:
            return f"write_final_answers() FAILED! {e}"

    def get_final_grade(message: Annotated[str, "Message for examiner"]) -> str:
        try:
            msg = MultipleChoice(
                    sender="student",
                    recepient="teacher",
                    prompt=message,
                    choices=["A", "B", "C", "D", "F"],
            )
            return io.process_message(msg)
        except Exception as e:
            return f"get_final_grade() FAILED! {e}"

    register_function(
        retrieve_exam_questions,
        caller=student_agent,
        executor=teacher_agent,
        name="retrieve_exam_questions",
        description="Get exam questions from examiner",
    )

    register_function(
        write_final_answers,
        caller=student_agent,
        executor=teacher_agent,
        name="write_final_answers",
        description="Write a final answers to exam questions to examiner, but only after discussing with the tutor first.",
    )

    register_function(
        get_final_grade,
        caller=student_agent,
        executor=teacher_agent,
        name="get_final_grade",
        description="Get the final grade after submitting the answers.",
    )

    chat_result = teacher_agent.initiate_chat(
        student_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary


from fastagency.core.io.console import ConsoleIO

app = FastAgency(wf=wf, io=ConsoleIO())
```

### Run Application

Once everything is set up, you can run your FastAgency application using the following command:

```console
fastagency run
```

#### Output
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
│ Starting a new workflow 'exam_practice' with the following                   │
│ description:                                                                 │
│                                                                              │
│ Student and teacher chat                                                     │
│                                                                              │
│ Please enter an initial                                                      │
│ message:                                                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
Let's start an exam about Leonardo da Vinci
    ╭─ Teacher_Agent -> Student_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ Let's start an exam about Leonardo da Vinci                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Student_Agent -> Teacher_Agent [suggested_function_call] ───────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "retrieve_exam_questions",                                │
    │   "call_id":                                                                 │
    │ "call_7vFfsdzfdsds",                                             │
    │   "arguments": {                                                             │
    │     "message":                                                               │
    │ "Please provide the exam questions about Leonardo da Vinci."                 │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ student -> teacher [text_input] ────────────────────────────────────────────╮
    │                                                                              │
    │ Please provide the exam questions about Leonardo da Vinci.                   │
    │ (suggestions: 1) Mona Lisa, 2) Innovations, 3) Florence at the time of       │
    │  Leonardo, 4) The Last Supper, 5) Vitruvian Man):                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯
1.
    ╭─ Teacher_Agent -> Student_Agent [function_call_execution] ───────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "retrieve_exam_questions",                                │
    │   "call_id":                                                                 │
    │ "call_7vFmsfgasfvsv",                                             │
    │   "retval": "1.\n"                                                           │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Student_Agent -> Teacher_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ I've received the first exam question. Please provide the question so        │
    │ I can draft a proposed answer.                                               │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Teacher_Agent -> Student_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ Sure! Here's the first exam question about Leonardo da Vinci:                │
    │                                                                              │
    │                                                                              │
    │ **Question 1:** What were some of Leonardo da Vinci's most significant       │
    │  contributions to art and science, and how did they influence the            │
    │ Renaissance period?                                                          │
    │                                                                              │
    │ Please draft your proposed answer based on this                              │
    │ question.                                                                    │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Student_Agent -> Teacher_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ Proposed Answer Draft:                                                       │
    │                                                                              │
    │ Leonardo da Vinci was a polymath whose                                       │
    │ contributions to art and science significantly shaped the Renaissance        │
    │ period. In art, his masterpieces such as the "Mona Lisa" and "The Last       │
    │  Supper" showcased innovative techniques like chiaroscuro (the use of        │
    │ light and shadow) and sfumato (the gradual blending of colors). These        │
    │ techniques not only enhanced the realism of his paintings but also           │
    │ influenced future generations of artists.                                    │
    │                                                                              │
    │ In science, da Vinci's                                                       │
    │ inquisitive nature and meticulous observations led him to study              │
    │ various fields, including anatomy, engineering, and botany. His              │
    │ anatomical sketches, based on dissections of human bodies, provided          │
    │ unprecedented insights into human physiology, laying foundational            │
    │ knowledge for modern medicine. Additionally, his designs for flying          │
    │ machines and war devices demonstrated a forward-thinking approach to         │
    │ engineering and invention.                                                   │
    │                                                                              │
    │ Da Vinci's synthesis of art and science                                      │
    │ exemplified the Renaissance ideal of humanism, emphasizing the               │
    │ potential of human creativity and intellect. His work inspired               │
    │ countless artists and scientists, making him a central figure in the         │
    │ cultural movement that defined the Renaissance.                              │
    │                                                                              │
    │ ---                                                                          │
    │                                                                              │
    │ What do you                                                                  │
    │ think of this draft? Would you like to add or modify anything?               │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Teacher_Agent -> Student_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ Your proposed answer draft is well-structured and covers key points          │
    │ about Leonardo da Vinci's contributions to both art and science, as          │
    │ well as their impact on the Renaissance. Here are a few suggestions to       │
    │  enhance it further:                                                         │
    │                                                                              │
    │ 1. **Introduction**: Consider adding a brief                                 │
    │ introductory sentence to set the context for your answer.                    │
    │                                                                              │
    │ 2.                                                                           │
    │ **Specific Techniques**: You might want to elaborate slightly on the         │
    │ significance of chiaroscuro and sfumato—maybe mention how these              │
    │ techniques contributed to emotional depth in his works.                      │
    │                                                                              │
    │ 3.                                                                           │
    │ **Influence on Future Generations**: You could mention specific              │
    │ artists influenced by da Vinci, such as Michelangelo or Raphael, to          │
    │ provide concrete examples of his legacy.                                     │
    │                                                                              │
    │ 4. **Conclusion**: A                                                         │
    │ concluding sentence that encapsulates his overall impact could               │
    │ strengthen the ending of your answer.                                        │
    │                                                                              │
    │ Here's an updated version                                                    │
    │ incorporating these suggestions:                                             │
    │                                                                              │
    │ ---                                                                          │
    │                                                                              │
    │ **Proposed Answer Draft                                                      │
    │ (Revised):**                                                                 │
    │                                                                              │
    │ Leonardo da Vinci was a polymath whose contributions to                      │
    │ art and science significantly shaped the Renaissance period, embodying       │
    │  the spirit of innovation and enquiry. In art, his masterpieces such         │
    │ as the "Mona Lisa" and "The Last Supper" showcased innovative                │
    │ techniques like chiaroscuro—enhancing the three-dimensionality of            │
    │ figures through light and shadow—and sfumato, which created soft             │
    │ transitions between colors and tones, adding emotional depth and             │
    │ realism. These techniques not only revolutionized painting during his        │
    │ time but also set new standards for artists in the generations that          │
    │ followed, influencing the works of greats like Michelangelo and              │
    │ Raphael.                                                                     │
    │                                                                              │
    │ In the realm of science, da Vinci's inquisitive nature and                   │
    │ meticulous observations led him to explore various fields, including         │
    │ anatomy, engineering, and botany. His detailed anatomical sketches,          │
    │ based on dissections of human bodies, provided unprecedented insights        │
    │ into human physiology, laying foundational knowledge that would inform       │
    │  modern medicine. Additionally, his visionary designs for flying             │
    │ machines and war devices demonstrated a remarkable forward-thinking          │
    │ approach to engineering and invention, anticipating many concepts that       │
    │  would only come to fruition centuries later.                                │
    │                                                                              │
    │ Da Vinci's synthesis of                                                      │
    │  art and science exemplified the Renaissance ideal of humanism,              │
    │ emphasizing the potential of human creativity and intellect. His             │
    │ groundbreaking work not only inspired countless artists and                  │
    │ scientists, but also established him as a central figure in the              │
    │ cultural movement that defined the Renaissance, leaving a lasting            │
    │ legacy that continues to resonate today.                                     │
    │                                                                              │
    │ ---                                                                          │
    │                                                                              │
    │ Feel free to use this                                                        │
    │ revised version or mix and match with your original draft as you see         │
    │ fit!                                                                         │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Student_Agent -> Teacher_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ What do you think of this revised version? Would you like to make any        │
    │ additional changes or proceed with this answer?                              │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Teacher_Agent -> Student_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ Your revised version is excellent! It provides a comprehensive               │
    │ overview of Leonardo da Vinci's contributions and their significance         │
    │ during the Renaissance. The added context, specific examples, and            │
    │ enhanced clarity make your answer even stronger.                             │
    │                                                                              │
    │ I don't see any                                                              │
    │ additional changes needed; it's well-rounded and insightful. If you          │
    │ feel confident with it, I suggest proceeding with this answer. Great         │
    │ job! If you have any more questions or need further assistance, feel         │
    │ free to ask.                                                                 │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Student_Agent -> Teacher_Agent [suggested_function_call] ───────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "write_final_answers",                                    │
    │   "call_id":                                                                 │
    │ "call_w915dnGhwwVRuRkVyRRFNuPo",                                             │
    │   "arguments": {                                                             │
    │     "message":                                                               │
    │ "Leonardo da Vinci was a polymath whose contributions to art and             │
    │ science significantly shaped the Renaissance period, embodying the           │
    │ spirit of innovation and enquiry. In art, his masterpieces such as the       │
    │  \"Mona Lisa\" and \"The Last Supper\" showcased innovative techniques       │
    │  like chiaroscuro\u2014enhancing the three-dimensionality of figures         │
    │ through light and shadow\u2014and sfumato, which created soft                │
    │ transitions between colors and tones, adding emotional depth and             │
    │ realism. These techniques not only revolutionized painting during his        │
    │ time but also set new standards for artists in the generations that          │
    │ followed, influencing the works of greats like Michelangelo and              │
    │ Raphael.\n\nIn the realm of science, da Vinci's inquisitive nature and       │
    │  meticulous observations led him to explore various fields, including        │
    │ anatomy, engineering, and botany. His detailed anatomical sketches,          │
    │ based on dissections of human bodies, provided unprecedented insights        │
    │ into human physiology, laying foundational knowledge that would inform       │
    │  modern medicine. Additionally, his visionary designs for flying             │
    │ machines and war devices demonstrated a remarkable forward-thinking          │
    │ approach to engineering and invention, anticipating many concepts that       │
    │  would only come to fruition centuries later.\n\nDa Vinci's synthesis        │
    │ of art and science exemplified the Renaissance ideal of humanism,            │
    │ emphasizing the potential of human creativity and intellect. His             │
    │ groundbreaking work not only inspired countless artists and                  │
    │ scientists, but also established him as a central figure in the              │
    │ cultural movement that defined the Renaissance, leaving a lasting            │
    │ legacy that continues to resonate today."                                    │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ function call logger -> system [system_message] ────────────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "message": {                                                               │
    │     "operation": "storing final answers",                                    │
    │                                                                              │
    │ "content": "Leonardo da Vinci was a polymath whose contributions to          │
    │ art and science significantly shaped the Renaissance period, embodying       │
    │  the spirit of innovation and enquiry. In art, his masterpieces such         │
    │ as the \"Mona Lisa\" and \"The Last Supper\" showcased innovative            │
    │ techniques like chiaroscuro\u2014enhancing the three-dimensionality of       │
    │  figures through light and shadow\u2014and sfumato, which created soft       │
    │  transitions between colors and tones, adding emotional depth and            │
    │ realism. These techniques not only revolutionized painting during his        │
    │ time but also set new standards for artists in the generations that          │
    │ followed, influencing the works of greats like Michelangelo and              │
    │ Raphael.\n\nIn the realm of science, da Vinci's inquisitive nature and       │
    │  meticulous observations led him to explore various fields, including        │
    │ anatomy, engineering, and botany. His detailed anatomical sketches,          │
    │ based on dissections of human bodies, provided unprecedented insights        │
    │ into human physiology, laying foundational knowledge that would inform       │
    │  modern medicine. Additionally, his visionary designs for flying             │
    │ machines and war devices demonstrated a remarkable forward-thinking          │
    │ approach to engineering and invention, anticipating many concepts that       │
    │  would only come to fruition centuries later.\n\nDa Vinci's synthesis        │
    │ of art and science exemplified the Renaissance ideal of humanism,            │
    │ emphasizing the potential of human creativity and intellect. His             │
    │ groundbreaking work not only inspired countless artists and                  │
    │ scientists, but also established him as a central figure in the              │
    │ cultural movement that defined the Renaissance, leaving a lasting            │
    │ legacy that continues to resonate today."                                    │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Teacher_Agent -> Student_Agent [function_call_execution] ───────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "write_final_answers",                                    │
    │   "call_id":                                                                 │
    │ "call_w915dnGhwwVRuRkVyRRFNuPo",                                             │
    │   "retval": "Final answers stored.\n"                                        │
    │                                                                              │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Student_Agent -> Teacher_Agent [suggested_function_call] ───────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_final_grade",                                        │
    │   "call_id":                                                                 │
    │ "call_B4UwlhiebfNODjTw0jCcBWJi",                                             │
    │   "arguments": {                                                             │
    │     "message":                                                               │
    │ "Please provide the final grade for the exam on Leonardo da Vinci."          │
    │                                                                              │
    │ }                                                                            │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ student -> teacher [multiple_choice] ───────────────────────────────────────╮
    │                                                                              │
    │ Please provide the final grade for the exam on Leonardo da Vinci.            │
    │ (choices: A, B, C, D, F, default: None)                                      │
    ╰──────────────────────────────────────────────────────────────────────────────╯
A
    ╭─ Teacher_Agent -> Student_Agent [function_call_execution] ───────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_final_grade",                                        │
    │   "call_id":                                                                 │
    │ "call_B4UwlhiebfNODjTw0jCcBWJi",                                             │
    │   "retval": "A\n"                                                            │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Student_Agent -> Teacher_Agent [text_message] ──────────────────────────────╮
    │                                                                              │
    │ I received an "A" as the final grade for the exam on Leonardo da             │
    │ Vinci!                                                                       │
    │                                                                              │
    │ If you have any further questions or need assistance with                    │
    │ anything else, just let me know. Otherwise, I will terminate the chat        │
    │ now.                                                                         │
    │                                                                              │
    │ TERMINATE                                                                    │
    ╰──────────────────────────────────────────────────────────────────────────────╯

╭─ workflow -> user [workflow_completed] ──────────────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "result": "The conversation involved preparing for an exam about           │
│ Leonardo da Vinci, specifically answering a question about his               │
│ contributions to art and science during the Renaissance. The student         │
│ drafted a comprehensive answer that was revised with additional              │
│ context and examples based on the teacher's feedback. The final answer       │
│  was submitted, resulting in a grade of \"A\"."                              │
│ }                                                                            │
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
