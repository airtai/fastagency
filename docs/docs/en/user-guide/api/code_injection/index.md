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
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the `inject_params` function:

```python hl_lines="8"
{! docs_src/user_guide/code_injection/mesop_main.py [ln:1-11] !}
```

## Define Bank Savings Function

The `get_savings` function is the core of this workflow. It retrieves the user's savings based on the provided **bank** name and a **token**.

### Key Idea
- The **bank name** is passed to the **LLM** for reasoning and decision-making.
- **Tokens**, which are sensitive pieces of information, are **NEVER shared with the LLM**. Instead, they will be securely injected into the function later in the workflow using the `inject_params` mechanism.

This ensures that the function can access the required data without compromising the token's confidentiality.

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

### Step-by-Step Process:

1. **User Input Collection**:
    - At the beginning of the workflow, the user is prompted to provide:
        - **Bank Name**: The workflow asks, *"Enter your bank"*.
        - **Token**: The workflow then asks, *"Enter your token"*.

2. **Sensitive Data Handling**:
    - The token provided by the user is stored securely in a **context dictionary (`ctx`)**.
    - This token is **never shared with the LLM** and is only used internally within the workflow.

3. **Parameter Injection**:
    - Using `inject_params`, the sensitive `token` from the `ctx` dictionary is injected into the `get_savings` function.

4. **Agent Setup**:
    - Two agents are created to handle the workflow:
        - **UserProxyAgent**: Simulates the user's perspective, facilitating secure communication.
        - **ConversableAgent**: Acts as the banker agent, retrieving savings information based on the user's input.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:49-79] !}
```
