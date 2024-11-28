# Code Injection

Code injection is a way to securely connect external functions to agents in `AutoGen` without exposing sensitive data like passwords or tokens. This guide will show you how to use `FastAgency` to build workflows where sensitive information is handled safely, even when working with LLMs.

We’ll create a simple example: a banking agent that retrieves a user's balance. The cool part? Sensitive info like tokens is kept secure and is never shared with the language model. Instead, it’s injected directly into the function when needed.

## Why Use Code Injection?
When working with LLMs, security is a big deal. You don’t want things like passwords or tokens ending up in a conversation or being logged somewhere. Code injection solves this problem by keeping sensitive information out of reach while still letting your agents do their job.

Here’s what makes it useful:

- **It’s Secure**: Your private data stays private.
- **It’s Easy**: Functions can use secure data without needing a lot of extra setup.
- **It’s Flexible**: You can integrate all kinds of workflows safely.

In this guide, we’ll walk through setting everything up, creating a workflow, and running a secure application step-by-step. Let’s get started!

---

## Install

We will use [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

In this example, we will create Mesop application without authentication. To do so, select the following settings after running the `cookiecutter` command:

```console
  [1/5] project_name (My FastAgency App): My Bank App
  [2/5] project_slug (my_bank_app):
  [3/5] Select app_type
    1 - fastapi+mesop
    2 - mesop
    3 - nats+fastapi+mesop
    4 - fastapi
    Choose from [1/2/3/4] (1): 2
  [4/5] Select python_version
    1 - 3.12
    2 - 3.11
    3 - 3.10
    Choose from [1/2/3] (1): 2
  [5/5] Select authentication
    1 - basic
    2 - google
    3 - none
    Choose from [1/2/3] (1): 3
```

## Complete Workflow Code
The only file you need to modify to run the application is `my_bank_app/workflow.py`. Simply copy and paste the following content into the file:

<details>
<summary>workflow.py</summary>
```python
{! docs_src/user_guide/code_injection/workflow.py !}
```
</details>

## Step-by-Step Guide

### Imports
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md) function:

```python hl_lines="7"
{! docs_src/user_guide/code_injection/workflow.py [ln:1-8] !}
```

### Define the Bank Savings Function

The `get_balance` function is central to this workflow. It retrieves the user's balance based on the provided **username** name and **password**.

The key consideration here is that both username and password should **NEVER** be exposed to the LLM. Instead, they will be securely injected into the `get_balance` function later in the workflow using the [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md) mechanism, ensuring that sensitive information remains confidential while still allowing the function to access the required data.

```python
{! docs_src/user_guide/code_injection/workflow.py [ln:10-23] !}
```


### Configure the Language Model (LLM)
Here, the large language model is configured to use the `gpt-4o-mini` model, and the API key is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/code_injection/workflow.py [ln:26-34] !}
```

### Define the Workflow and Agents

The `bank_workflow` handles user interaction and integrates agents to retrieve balance securely.


1. **User Input Collection**:
    - At the beginning of the workflow, the user is prompted to provide:
        - **Username**: The workflow asks, *"Enter your username:"*.
        - **Password**: The workflow then asks, *"Enter your password:"*.

2. **Agent Setup**:
    - Two agents are created to handle the workflow:
        - **UserProxyAgent**: Simulates the user's perspective, facilitating secure communication.
        - **ConversableAgent**: Acts as the banker agent, retrieving the user's balance.

```python
{! docs_src/user_guide/code_injection/workflow.py [ln:36-63] !}
```

### Code Injection
The token provided by the user is stored securely in a **context dictionary (`ctx`)**.
This token is **never shared with the LLM** and is only used internally within the workflow.

Using [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md), the sensitive `token` from the `ctx` dictionary is injected into the `get_balance` function.

```python
{! docs_src/user_guide/code_injection/workflow.py [ln:65-69] !}
```

### Register Function with the Agents
In this step, we register the `get_balance_with_params`
```python
{! docs_src/user_guide/code_injection/workflow.py [ln:70-75] !}
```

### Enable Agent Interaction and Chat
Here, the user agent initiates a chat with the banker agent, which retrieves the user's balance. The conversation is summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/code_injection/workflow.py [ln:77-84] !}
```

## Run Application

You can run this chapter's FastAgency application using the following command:

```console
gunicorn my_bank_app.deployment.main:app
```

## Output
At the beginning, the user is asked to provide the **username** and **password**.

![User Input](./images/user_input.png)

Once the user provides the information, the agent executes the `get_balance` function with both parameters securely injected into the function using the [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md) mechanism, ensuring the token is not exposed to the LLM.

The agent processes the request, retrieves the user's balance, and provides a summary of the results without compromising sensitive data.

![Result](./images/result.png)
