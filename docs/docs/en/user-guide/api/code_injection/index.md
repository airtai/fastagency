# Code Injection

This guide explains how to integrate external functions into `AutoGen` agents using **code injection** with `FastAgency`. We'll create a banking agent that securely accesses user savings through injected parameters. The example includes setting up agents, registering functions, and facilitating conversations between agents.

---

## Install

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**. Before getting started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```console
pip install "fastagency[autogen,mesop]"
```

## Imports
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md) function:

```python hl_lines="8"
{! docs_src/user_guide/code_injection/mesop_main.py [ln:1-11] !}
```

## Define the Bank Savings Function

The `get_savings` function is central to this workflow. It retrieves the user's savings based on the provided **bank** name and **token**.

The key consideration here is that the **token** should NEVER be exposed to the LLM. Instead, the **token** will be securely injected into the `get_savings` function later in the workflow using the [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md) mechanism, ensuring that sensitive information remains confidential while still allowing the function to access the required data.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:12-35] !}
```


## Configure the Language Model (LLM)
Here, the large language model is configured to use the `gpt-4o-mini` model, and the API key is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:38-46] !}
```

## Define the Workflow and Agents

The `banking_workflow` handles user interaction and integrates agents to retrieve savings securely.


1. **User Input Collection**:
    - At the beginning of the workflow, the user is prompted to provide:
        - **Bank Name**: The workflow asks, *"Enter your bank"*.
        - **Token**: The workflow then asks, *"Enter your token"*.

2. **Agent Setup**:
    - Two agents are created to handle the workflow:
        - **UserProxyAgent**: Simulates the user's perspective, facilitating secure communication.
        - **ConversableAgent**: Acts as the banker agent, retrieving savings information based on the user's input.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:49-76] !}
```

## Code Injection
The token provided by the user is stored securely in a **context dictionary (`ctx`)**.
This token is **never shared with the LLM** and is only used internally within the workflow.

Using [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md), the sensitive `token` from the `ctx` dictionary is injected into the `get_savings` function.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:78-79] !}
```

## Register Function with the Agents
In this step, we register the `get_savings_with_params`
```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:80-85] !}
```

## Enable Agent Interaction and Chat
Here, the user agent initiates a chat with the banker agent, which retrieves information about the savings. The conversation is summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:87-95] !}
```

## Define FastAgency Application

Next, define your FastAgency application.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:98] !}
```

## Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/code_injection/mesop_main.py !}
```
</details>


## Run Application

You can run this chapter's FastAgency application using the following command:

```console
fastagency run
```

## Output
At the beginning, the user is asked to provide the **bank name** and **token**.

![User Input](./images/user_input.png)

Once the user provides the information, the agent executes the `get_savings` function with the **bank name** as a parameter.
The **token** is securely injected into the function using the [**`inject_params`**](../../../api/fastagency/api/code_injection/inject_params.md) mechanism, ensuring the token is not exposed to the LLM.

The agent processes the request, retrieves the user's savings information, and provides a summary of the results without compromising sensitive data.

![Result](./images/result.png)
