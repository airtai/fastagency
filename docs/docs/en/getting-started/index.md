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

<!--
  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/airtai/fastagency" target="_blank">
      <img src="https://coverage-badge.samuelcolvin.workers.dev/airtai/fastagency.svg" alt="Coverage">
  </a>
 -->

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

Welcome to FastAgency! This guide will walk you through the initial setup and usage of FastAgency, a powerful tool that leverages the AutoGen framework to quickly build applications. FastAgency is designed to be flexible and adaptable, and we plan to extend support to additional agentic frameworks such as [CrewAI](https://www.crewai.com/){target="_blank"} in the near future. This will provide even more options for defining workflows and integrating with various AI tools.

With FastAgency, you can create interactive applications using various interfaces such as a console or Mesop.

## Supported Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [ConsoleIO](../api/fastagency/core/io/console/ConsoleIO.md) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.
- **Mesop**: Utilize [Mesop](https://google.github.io/mesop/){target="_blank"} with [MesopIO](../api/fastagency/core/io/mesop/MesopIO.md) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

We are also working on adding support for other frameworks, such as [CrewAI](https://www.crewai.com/){target="_blank"}, to broaden the scope and capabilities of FastAgency. Stay tuned for updates on these integrations.

## Quick start

### Install

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

!!! note "Using older AutoGen version 0.2.x"

    In case you want to use an older version of AutoGen (`pyautogen` instead of `autogen` package ), please use the following pip command:

    === "Console"
        ```console
        pip install "fastagency[pyautogen]"
        ```

        This command installs FastAgency with support for the Console interface and AutoGen framework.

    === "Mesop"
        ```console
        pip install "fastagency[pyautogen,mesop]"
        ```


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

### Run Application

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

FastAgency can automatically create functions properly annotated for use with LLM-s from [OpenAPI](https://swagger.io/specification/) specification.

This example demonstrates how to integrate external REST API calls into `AutoGen` agents using `FastAgency`. We'll create a weather agent that interacts with a weather REST API and a user agent to facilitate the conversation. This example will help you understand how to set up agents and facilitate agent communication through an external REST API. To interact with the REST API, the AutoGen agent needs to understand the available routes, so it requires the OpenAPI specification (`openapi.json` file) for the external REST API.

In this example, we'll use a simple [weather API](https://weather.tools.fastagency.ai/docs){target="_blank"} and its specification available at [https://weather.tools.fastagency.ai/openapi.json](https://weather.tools.fastagency.ai/openapi.json){target="_blank"}.

### Install

To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```console
pip install "fastagency[autogen,openapi]"
```

### Imports
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

### Define Workflow

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

### Run Application

Once everything is set up, you can run your FastAgency application using the following command:

```console
fastagency run
```

## Custom User Interactions

In this example, we'll demonstrate how to create custom interaction with the user using [`Chatable`](../api/fastagency/core/Chatable.md) protocol and its [`process_message`](../api/fastagency/core/Chatable.md#fastagency.core.Chatable.create_subconversation) method.


### Define Interaction

This section describes how to define functions for the `ConversableAgent` instances representing the student and teacher. We will also explain the differences between `MultipleChoice`, `SystemMessage`, and `TextInput`, which are used for communication between the user and agents.

Let's define three functions which will be available to the agents:

#### Free Textual Tnput

`TextInput` is suitable for free-form text messages, ideal for open-ended queries and dialogues. This function allows the student to request exam questions from the teacher and provides some suggestions using `TextInput`.

```python
def retrieve_exam_questions(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = TextInput(
            sender="student",
            recipient="teacher",
            prompt=message,
            suggestions=["1) Mona Lisa", "2) Innovations", "3) Florence at the time of Leonardo", "4) The Last Supper", "5) Vitruvian Man"],
        )
        return io.process_message(msg)
    except Exception as e:
        return f"retrieve_exam_questions() FAILED! {e}"
```

#### System Info Messages

`SystemMessage` is used for operational or system-related instructions, such as logging data, and is not part of the agent dialogue. This function logs the final answers after the student completes the discussion using `SystemMessage` to log the event.

```python
def write_final_answers(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = SystemMessage(
            sender="function call logger",
            recipient="system",
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

#### Multiple Choice

`MultipleChoice` is used for structured responses where the user must select one of several predefined options. This function retrieves the final grade for the student's submitted answers using `MultipleChoice`, presenting the user with grading options.

```python
def get_final_grade(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = MultipleChoice(
            sender="student",
            recipient="teacher",
            prompt=message,
            choices=["A", "B", "C", "D", "F"],
        )
        return io.process_message(msg)
    except Exception as e:
        return f"get_final_grade() FAILED! {e}"
```

#### Other Types of Messages

All supported messages are subclasses of the [IOMessage](../api/fastagency/core/IOMessage.md) base class.

### Registering the Functions
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
                recipient="teacher",
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
                recipient="system",
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
                    recipient="teacher",
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

## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, such as [CrewAI](https://www.crewai.com/){target="_blank"}, to provide more flexibility and options for building applications. This will allow you to define workflows using a variety of frameworks and leverage their unique features and functionalities.

Feel free to customize your workflow and application based on your needs. For more details on configurations and additional features, refer to the [AutoGen documentation](https://autogen-ai.github.io/autogen/){target="_blank"} and [Mesop documentation](https://google.github.io/mesop/){target="_blank"}.

---

## Stay in touch

Please show your support and stay in touch by:

- giving our [GitHub repository](https://github.com/airtai/fastagency/){target="_blank"} a star, and

- joining our [Discord server](https://discord.gg/kJjSGWrknU){target="_blank"}

Your support helps us to stay in touch with you and encourages us to
continue developing and improving the framework. Thank you for your
support!

---

## Contributors

Thanks to all of these amazing people who made the project better!

<a href="https://github.com/airtai/fastagency/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=airtai/fastagency"/>
</a>
