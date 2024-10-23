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

## What is FastAgency?

For start, FastAgency is not yet another agentic AI framework. There are many such
frameworks available today, the most popular open-source ones being [**AutoGen**](https://github.com/microsoft/autogen), [**CrewAI**](https://www.crewai.com/), [**Swarm**](https://github.com/openai/swarm) and [**LangGraph**](https://github.com/langchain-ai/langgraph). FastAgency provides you with a unified programming interface for deploying agentic workflows written in above agentic frameworks in both development and productional settings (current version supports [**AutoGen**](https://github.com/microsoft/autogen) only, but other frameworks will be supported very soon). With only a few lines of code, you can create a web chat application or REST API service interacting with agents of your choice. If you need to scale-up your workloads, FastAgency can help you deploy a fully distributed system using internal message brokers coordinating multiple machines in multiple datacenters with just a few lines of code changed from your local development setup.

In the rest of this guide, we will walk you through the initial setup and usage of FastAgency, using both development and production environments.

### Supported Runtimes

Currently, the only supported runtime is [**AutoGen**](https://github.com/microsoft/autogen), with support for [**CrewAI**](https://www.crewai.com/), [**Swarm**](https://github.com/openai/swarm) and [**LangGraph**](https://github.com/langchain-ai/langgraph) coming soon.

### Supported User Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [**`ConsoleUI`**](https://fastagency.ai/0.3/api/fastagency/ui/console/ConsoleUI/) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.

- [**Mesop**](https://google.github.io/mesop/): Utilize [**`MesopUI`**](https://fastagency.ai/0.3/api/fastagency/ui/mesop/MesopUI/) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

### Supported Network Adapters

FastAgency can use chainable network adapters that can be used to easily create
scalable, production ready architectures for serving your workflows. Currently, we
support the following network adapters:

- [**REST API**](https://en.wikipedia.org/wiki/REST) via [**FastAPI**](https://fastapi.tiangolo.com/): Use the [**`FastAPIAdapter`**](https://fastagency.ai/0.3/api/fastagency/adapters/fastapi/FastAPIAdapter/) to serve your workflow using [**FastAPI**](https://fastapi.tiangolo.com/) server. This setup allows you to work your workflows in multiple workers and serve them using the highly extensible and stable ASGI server.

- [**NATS.io**](https://nats.io/) via [**FastStream**](https://github.com/airtai/faststream): Utilize the [**`NatsAdapter`**](https://fastagency.ai/0.3/api/fastagency/adapters/nats/NatsAdapter/) to use [**NATS.io MQ**](https://nats.io/) message broker for highly-scalable, production-ready setup. This interface is suitable for setups in VPN-s or, in combination with the [**`FastAPIAdapter`**](https://fastagency.ai/0.3/api/fastagency/adapters/fastapi/FastAPIAdapter/) to serve public workflows in an authenticated, secure manner.

## Quick start

There are four different setups, two for development and two for production workloads:

- Development setups

    - **Console**: This setup uses console for interactively executing your workflow.
        It is also very useful for automating testing and integration with CI/CD.


    - **Mesop**: This setup uses [**Mesop**](https://google.github.io/mesop/)
        to build a web application for interacting with our workflow. It supports
        a single-worker deployments only, limiting its scalability. However, it
        is the fastest way to debug your application.

- Production setups

    - **FastAPI + Mesop**: This is fairly scalable setup using [**FastAPI**](https://fastapi.tiangolo.com/)
         to execute your workflows and [**Mesop**](https://google.github.io/mesop/) for interactive web application. [**FastAPI**](https://fastapi.tiangolo.com/) supports execution with multiple workers with each workflowe being executed in the context of a websocket connection. [**Mesop**](https://google.github.io/mesop/) is still limited to a single worker, although there is much less load of it due to workflows being executed in the [**FastAPI**](https://fastapi.tiangolo.com/) workers.

    - **NATS + FastAPI + Mesop**: This is the most scalable setup using a distributed message broker
        [**NATS.io MQ**](https://nats.io/). Workflows are being executed with
        multiple workers that attach to the MQ waiting for initiate workflow messages. Such workers
        can be running on different machines or even different data centers/cloud providers.
        Message queues are highly scalable, but more difficult to integrate with end-clients.
        In order to make such integrations easier, we will connect our [**NATS**](https://nats.io/)-based message queue with the [**FastAPI**](https://fastapi.tiangolo.com/)
         application.

We will show you how to deploy your workflow using the **FastAPI + Mesop** combination below.

### Install

To get started, you need to install FastAgency. You can do this using `pip`, Python's package installer. Choose the installation command based on the interface you want to use:

```console
pip install "fastagency[autogen,mesop,fastapi,server]"
```

This command installs FastAgency with support for both the Console and Mesop
interfaces for AutoGen workflows, but with FastAPI both serving input requests
and running workflows.


### Imports
Depending on the interface you choose, you'll need to import different modules. These imports set up the necessary components for your application:

```python
import os
from typing import Any

from autogen.agentchat import ConversableAgent
from fastapi import FastAPI

from fastagency import UI
from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.runtimes.autogen import AutoGenWorkflows
```

For FastAPI applications, import `FastAPIAdapter` to expose your workflows as REST API.

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
def simple_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you learn about mathematics. What subject you would like to explore?",
    )

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


In the case of FastAPI application, we will create an `FastAPIAdapter` and then include a router to the `FastAPI` application.
The adapter will have all REST and Websocket routes for communicating with a client.

```python
adapter = FastAPIAdapter(provider=wf)

app = FastAPI()
app.include_router(adapter.router)
```

### Adapter Chaining

There is an additional specification file for an application using `MesopUI`
to connect to the `FastAPIAdapter`

#### `main_2_mesop.py`
```python
from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.app import FastAgency
from fastagency.ui.mesop import MesopUI

fastapi_url = "http://localhost:8008"

provider = FastAPIAdapter.create_provider(
    fastapi_url=fastapi_url,
)

app = FastAgency(provider=provider, ui=MesopUI())
```


### Complete Application Code

#### `main_1_fastapi.py`

```python
import os
from typing import Any

from autogen.agentchat import ConversableAgent
from fastapi import FastAPI

from fastagency import UI
from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.runtimes.autogen import AutoGenWorkflows

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
def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you learn about mathematics. What subject you would like to explore?",
    )

    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
        llm_config=llm_config,
        # human_input_mode="ALWAYS",
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
        llm_config=llm_config,
        # human_input_mode="ALWAYS",
    )

    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )

    return chat_result.summary  # type: ignore[no-any-return]


adapter = FastAPIAdapter(provider=wf)

app = FastAPI()
app.include_router(adapter.router)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def read_root() -> dict[str, dict[str, str]]:
    return {"Workflows": {name: wf.get_description(name) for name in wf.names}}


# start the provider with the following command
# uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
```

#### `main_2_mesop.py`

```python
from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.app import FastAgency
from fastagency.ui.mesop import MesopUI

fastapi_url = "http://localhost:8008"

provider = FastAPIAdapter.create_provider(
    fastapi_url=fastapi_url,
)

app = FastAgency(provider=provider, ui=MesopUI())

# start the provider with the following command
# gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
```

### Run Application

In this setup, we need to run **two** commands in **separate** terminal windows:

**Terminal 1** - Start **FastAPI** application using uvicorn
```
uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
```

**Terminal 2** - Start **Mesop** web interface using gunicorn
```
gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
```

### Output

The outputs will vary based on the interface, here is the output of the last terminal starting UI:

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8888 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

![Initial message](https://fastagency.ai/0.3/getting-started/images/chat.png?v20241015)


## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, other network provider and other UI frameworks.

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
