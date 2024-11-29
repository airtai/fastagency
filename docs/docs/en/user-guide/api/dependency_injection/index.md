# Dependency Injection

[Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection){target="_blank"} is a secure way to connect external functions to agents in `AutoGen` without exposing sensitive data such as passwords, tokens, or personal information. This approach ensures that sensitive information remains protected while still allowing agents to perform their tasks effectively, even when working with large language models (LLMs).

In this guide, we’ll explore how to use `FastAgency` to build secure workflows that handle sensitive data safely.

As an example, we’ll create a banking agent that retrieves a user's account balance. The best part is that sensitive data like username and password are never shared with the language model. Instead, it’s securely injected directly into the function at runtime, keeping it safe while maintaining seamless functionality.

Let’s get started!


## Why Use Dependency Injection?

When working with large language models (LLMs), **security is paramount**. There are several types of sensitive information that we want to keep out of the LLM’s reach:

- **Passwords or tokens**: These could be exposed through [prompt injection attacks](https://en.wikipedia.org/wiki/Prompt_injection){target="_blank"}.
- **Personal information**: Access to this data might fall under strict regulations, such as the [EU AI Act](https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence){target="_blank"}.

Dependency injection offers a robust solution by isolating sensitive data while enabling your agents to function effectively.

## Why Dependency Injection Is Essential

Here’s why dependency injection is a game-changer for secure LLM workflows:

- **Enhanced Security**: Your sensitive data is never directly exposed to the LLM.
- **Simplified Development**: Secure data can be seamlessly accessed by functions without requiring complex configurations.
- **Unmatched Flexibility**: It supports safe integration of diverse workflows, allowing you to scale and adapt with ease.

In this guide, we’ll explore how to set up dependency injection, build secure workflows, and create a protected application step-by-step. Let’s dive in!

---

## Install

We will use [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

In this example, we’ll create a **Mesop** application **without authentication**. The generated project will have the following files:

```console
{! docs_src/user_guide/dependency_injection/mesop/folder_structure.txt !}
```

## Complete Workflow Code
The only file you need to modify to run the application is `my_bank_app/my_bank_app/workflow.py`. Simply copy and paste the following content into the file:

<details>
<summary>workflow.py</summary>
```python
{! docs_src/user_guide/dependency_injection/workflow.py !}
```
</details>

## Step-by-Step Guide

### Imports
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the [**`inject_params`**](../../../api/fastagency/api/dependency_injection/inject_params.md) function:

```python hl_lines="7"
{! docs_src/user_guide/dependency_injection/workflow.py [ln:1-8] !}
```

### Define the Bank Savings Function

The `get_balance` function is central to this workflow. It retrieves the user's balance based on the provided **username** and **password**.

The key consideration here is that both username and password should **NEVER** be exposed to the LLM. Instead, they will be securely injected into the `get_balance` function later in the workflow using the [**`inject_params`**](../../../api/fastagency/api/dependency_injection/inject_params.md) mechanism, ensuring that sensitive information remains confidential while still allowing the function to access the required data.

```python
{! docs_src/user_guide/dependency_injection/workflow.py [ln:10-23] !}
```


### Configure the Language Model (LLM)
Here, the large language model is configured to use the `gpt-4o-mini` model, and the API key is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/dependency_injection/workflow.py [ln:26-34] !}
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
{! docs_src/user_guide/dependency_injection/workflow.py [ln:36-63] !}
```

### Dependency Injection
Username and password provided by the user are stored securely in a **context dictionary (`ctx`)**.
These parameters are **never shared with the LLM** and they are only used internally within the workflow.

Using [**`inject_params`**](../../../api/fastagency/api/dependency_injection/inject_params.md), the sensitive parameters from the `ctx` dictionary are injected into the `get_balance` function.

```python
{! docs_src/user_guide/dependency_injection/workflow.py [ln:65-69] !}
```

### Register Function with the Agents
In this step, we register the `get_balance_with_params`
```python
{! docs_src/user_guide/dependency_injection/workflow.py [ln:70-75] !}
```

### Enable Agent Interaction and Chat
Here, the user agent initiates a chat with the banker agent, which retrieves the user's balance. The conversation is summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/dependency_injection/workflow.py [ln:77-84] !}
```

## Run Application

You can run this chapter's FastAgency application using the following command:

```console
gunicorn my_bank_app.deployment.main:app
```

## Output
At the beginning, the user is asked to provide the **username** and **password**.

![User Input](./images/user_input.png)

Once the user provide them, the agent executes the `get_balance` function with both parameters securely injected into the function using the [**`inject_params`**](../../../api/fastagency/api/dependency_injection/inject_params.md) mechanism, ensuring these parameters are not exposed to the LLM.

The agent processes the request, retrieves the user's balance, and provides a summary of the results without compromising sensitive data.

![Result](./images/result.png)
