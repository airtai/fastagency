![alt text](https://github.com/airtai/fastagency/blob/main/docs/docs/assets/img/FA-Secondary-LOGO.jpg?raw=true)


# FastAgency

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

Welcome to FastAgency! This guide will walk you through the initial setup and usage of FastAgency, a powerful tool that leverages the AutoGen framework to quickly build applications. FastAgency is designed to be flexible and adaptable, and we plan to extend support to additional agentic frameworks such as [CrewAI](https://www.crewai.com/) in the near future. This will provide even more options for defining workflows and integrating with various AI tools.

With FastAgency, you can create interactive applications using various interfaces such as a console or Mesop.

## Supported Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [ConsoleUI](https://fastagency.ai/0.2/api/fastagency/ui/console/ConsoleUI.md) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.
- **Mesop**: Utilize [Mesop](https://google.github.io/mesop/) with [MesopUI](https://fastagency.ai/0.2/api/fastagency/ui/mesop/MesopUI.md) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

We are also working on adding support for other frameworks, such as [CrewAI](https://www.crewai.com/), to broaden the scope and capabilities of FastAgency. Stay tuned for updates on these integrations.

## Quick start

### Install

To get started, you need to install FastAgency. You can do this using `pip`, Python's package installer. This command installs FastAgency with support for the [Mesop](https://google.github.io/mesop/) interface and AutoGen framework.

```console
pip install "fastagency[autogen,mesop]"
```

## Write Code

### Imports
Depending on the interface you choose, you'll need to import different modules. These imports set up the necessary components for your application:

```python
import os

from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency, Workflows
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI
```


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
    "temperature": 0.0,
}

wf = AutoGenWorkflows()


@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(
    wf: Workflows, ui: UI, initial_message: str, session_id: str
) -> str:
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
        max_turns=3,
    )

    return chat_result.summary
```

This code snippet sets up a simple learning chat between a student and a teacher. You define the agents and how they should interact, specifying how the conversation should be summarized.

### Define FastAgency Application

Next, define your FastAgency application. This ties together your workflow and the interface you chose:

```python
app = FastAgency(wf=wf, ui=MesopUI(), title="Learning Chat")
```

## Run Application

Once everything is set up, you can run your FastAgency application using the following command:

  ```
  fastagency run
  ```

  However, the preferred way of running Mesop application is a Python WSGI HTTP Server such as [Gunicorn](https://gunicorn.org/). First,
  you need to install it using package manager such as `pip`:
  ```
  pip install gunicorn
  ```
  and then you can run it with:
  ```
  gunicorn main:app
  ```

### Output

  ```console
  [2024-10-01 16:18:59 +0000] [20390] [INFO] Starting gunicorn 23.0.0
  [2024-10-01 16:18:59 +0000] [20390] [INFO] Listening at: http://127.0.0.1:8000 (20390)
  [2024-10-01 16:18:59 +0000] [20390] [INFO] Using worker: sync
  [2024-10-01 16:18:59 +0000] [20391] [INFO] Booting worker with pid: 20391
  ```

  ![Initial message](https://fastagency.ai/0.2/getting-started/images/chat.png?v1)



## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, such as [CrewAI](https://www.crewai.com/), to provide more flexibility and options for building applications. This will allow you to define workflows using a variety of frameworks and leverage their unique features and functionalities.

---

## Documentation

You can find detailed documentation on the following link: [fastagency.ai/latest](fastagency.ai/latest).

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

<a href="https://github.com/airtai/fastagency/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=airtai/fastagency"/>
</a>
