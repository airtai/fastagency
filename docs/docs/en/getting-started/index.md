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

Welcome to FastAgency! This guide will walk you through the initial setup and usage of FastAgency, a powerful tool that leverages the AutoGen framework to quickly build applications. FastAgency is designed to be flexible and adaptable, and we plan to extend support to additional agentic frameworks such as [CrewAI](https://www.crewai.com/){target="_blank"} in the near future. This will provide even more options for defining workflows and integrating with various AI tools.

With FastAgency, you can create interactive applications using various interfaces such as a console or Mesop.

## Supported Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [ConsoleUI](../api/fastagency/ui/console/ConsoleUI.md) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.
- **Mesop**: Utilize [Mesop](https://google.github.io/mesop/){target="_blank"} with [MesopUI](../api/fastagency/ui/mesop/MesopUI.md) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

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
    ```python hl_lines="8"
    {!> docs_src/getting_started/main_console.py [ln:1-8] !}
    ```

    For Console applications, import `ConsoleUI` to handle command-line input and output.

=== "Mesop"
    ```python hl_lines="8"
    {!> docs_src/getting_started/main_mesop.py [ln:1-8] !}
    ```

    For Mesop applications, import `MesopUI` to integrate with the Mesop web interface.

### Define Workflow

You need to define the workflow that your application will use. This is where you specify how the agents interact and what they do. Here's a simple example of a workflow definition:

```python
{! docs_src/getting_started/main_console.py [ln:9-53] !}
```

This code snippet sets up a simple learning chat between a student and a teacher. You define the agents and how they should interact, specifying how the conversation should be summarized.

### Define FastAgency Application

Next, define your FastAgency application. This ties together your workflow and the interface you chose:

=== "Console"
    ```python hl_lines="1"
    {!> docs_src/getting_started/main_console.py [ln:55] !}
    ```

    For Console applications, use `ConsoleUI` to handle user interaction via the command line.

=== "Mesop"
    ```python hl_lines="1"
    {!> docs_src/getting_started/main_mesop.py [ln:55] !}
    ```

    For Mesop applications, use `MesopUI` to enable web-based interactions.


## Complete Application Code

=== "Console"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/getting_started/main_console.py !}
        ```
    </details>

=== "Mesop"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/getting_started/main_mesop.py !}
        ```
    </details>

### Run Application

Once everything is set up, you can run your FastAgency application using the following command:

=== "Console"

    ```console
    fastagency run
    ```

=== "Mesop"

    ```
    fastagency run
    ```

    However, the preferred way to run the Mesop application is using a Python WSGI HTTP server like [Gunicorn](https://gunicorn.org/). First,
    you need to install it using package manager such as `pip`:
    ```
    pip install gunicorn
    ```
    and then you can run it with:
    ```
    gunicorn main:app
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

    ╭─ FastAgency -> user [workflow_started] ──────────────────────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "name": "simple_learning",                                                 │
    │   "description": "Student and teacher                                        │
    │ learning chat",                                                              │
    │   "params": {}                                                               │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you learn about geometry. What subject you would like to          │
    │ explore?:                                                                    │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

    For Console applications, you will see a command-line prompt where you can enter the initial message and interact with your workflow.

=== "Mesop"
    ```console
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8000 (23635)
    [2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
    [2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
    ```

    ![Initial message](./images/chat.png)



## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, such as [CrewAI](https://www.crewai.com/){target="_blank"}, to provide more flexibility and options for building applications. This will allow you to define workflows using a variety of frameworks and leverage their unique features and functionalities.

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
