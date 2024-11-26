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

```python hl_lines="9"
{! docs_src/user_guide/code_injection/mesop_main.py [ln:1-11] !}
```

## Define Bank Savings Function

The `get_savings` function is the core of this workflow. It retrieves the user's savings based on the provided **bank** name and a **token**.

### Key Idea:
- The **bank name** is passed to the **LLM** for reasoning and decision-making.
- **Tokens**, which are sensitive pieces of information, are **never shared with the LLM**. Instead, they are securely injected into the function using the `inject_params` mechanism.
This ensures that the function can access the required data without compromising the token's confidentiality.

```python
{! docs_src/user_guide/code_injection/mesop_main.py [ln:13-32] !}
```
