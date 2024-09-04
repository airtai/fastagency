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

# Getting Started

Welcome to FastAgency! This guide will walk you through the initial setup and usage of FastAgency, a powerful tool that leverages the [AutoGen](https://microsoft.github.io/autogen/) framework to quickly build applications. FastAgency is designed to be flexible and adaptable, and we plan to extend support to additional agentic frameworks such as [CrewAI](https://www.crewai.com/) in the near future. This will provide even more options for defining workflows and integrating with various AI tools.

With FastAgency, you can create interactive applications using various interfaces such as a console or Mesop.

## Supported Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [Console](/api/fastagency/core/io/console/ConsoleIO/) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.
- **Mesop**: Utilize [Mesop](https://google.github.io/mesop/) with [MesopIO](/api/fastagency/core/io/mesop/MesopIO/) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

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

    +--------------------------------------------------------------------------------+
    |
    | FastAgency -> user: text_input
    |
    | Starting a new workflow 'simple_learning' with the following
    | description:
    |
    | Student and teacher learning chat
    |
    | Please enter an
    | initial message: (suggestions: )
    +--------------------------------------------------------------------------------+
    ```

    For Console applications, you will see a command-line prompt where you can enter the initial message and interact with your workflow.

=== "Mesop"
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

    Mesop app running at: http://127.0.0.1:8000/
    ```

    For Mesop applications, the output will include a URL where you can access your web-based application.

## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, such as [CrewAI](https://www.crewai.com/), to provide more flexibility and options for building applications. This will allow you to define workflows using a variety of frameworks and leverage their unique features and functionalities.

Feel free to customize your workflow and application based on your needs. For more details on configurations and additional features, refer to the [AutoGen documentation](https://microsoft.github.io/autogen/) and [Mesop documentation](https://google.github.io/mesop/).
