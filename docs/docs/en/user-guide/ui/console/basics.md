# Console

**[ConsoleUI](../../../../api/fastagency/ui/console/ConsoleUI.md)** in FastAgency provides a text-based interface for interacting with multi-agent workflows directly from the command line. This interface allows developers to quickly test and prototype workflows without needing to set up a graphical or web-based interface, making it an excellent tool for early-stage development and debugging.

Below is an example that demonstrates how to set up a simple learning conversation between a student and a teacher using **[ConsoleUI](../../../../api/fastagency/ui/console/ConsoleUI.md)**.

## Installation

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**. Before getting started, make sure you have installed FastAgency with support for the AutoGen runtime by running the following command:

```bash
pip install "fastagency[autogen]"
```

This installation includes the AutoGen runtime, allowing you to build multi-agent workflows and integrate external APIs seamlessly.

## Example: Student and Teacher Learning Chat

This example demonstrates how to create a workflow where a student agent interacts with a teacher agent. The student asks questions, and the teacher provides responses, simulating a learning environment. The interaction is facilitated through the console using **[ConsoleUI](../../../../api/fastagency/ui/console/ConsoleUI.md)**.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
We begin by importing the necessary modules from **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating the ConsoleUI.

```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/workflow.py [ln:1-6] !}
```

- **ConversableAgent**: This class allows the creation of agents that can engage in conversational tasks.
- **[FastAgency](../../../../api/fastagency/FastAgency.md)**: The core class responsible for orchestrating workflows and connecting them with UIs.
- **[UI](../../../../api/fastagency/UI.md)** and **[ConsoleUI](../../../../api/fastagency/ui/console/ConsoleUI.md)**: These classes define the user interface for interaction, with ConsoleUI providing a text-based interface.
- **[AutoGenWorkflows](../../../../api/fastagency/runtimes/autogen/AutoGenWorkflows.md)**: Manages the creation and execution of multi-agent workflows.

#### 2. **Configure the Language Model (LLM)**
Next, we configure the language model that will power the agents. In this case, we're using **gpt-4o-mini**, and the API key is retrieved from the environment.

```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/workflow.py [ln:8-17] !}
```

- **Explanation**: The configuration specifies the LLM model and API key used for powering the conversation between agents. The temperature is set to `0.0` to ensure deterministic responses from the agents, making interactions consistent and reliable. This is particularly useful for scenarios where repeatability and predictability are required, such as testing.

#### 3. **Define the Workflow and Agents**
Here, we define a simple workflow where the **Student Agent** interacts with the **Teacher Agent**. The student asks questions, and the teacher responds as a math teacher. The workflow is registered using **AutoGenWorkflows**.

```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/workflow.py [ln:18-48] !}
```

- **Agent Overview**: The **Student Agent** is configured with a system message, "You are a student willing to learn," and will initiate questions during the interaction. The **Teacher Agent**, on the other hand, is set up as a math teacher and will respond to the student's questions.
- **Workflow Registration**: The workflow is registered under the name `simple_learning`. The **ConversableAgent** class is used to represent both the student and teacher agents, allowing them to communicate with each other up to 5 turns before summarizing the conversation using the `reflection_with_llm` method.

#### 4. **Using ConsoleUI**
Finally, we instantiate **[ConsoleUI](../../../../api/fastagency/ui/console/ConsoleUI.md)** to link the workflow to a text-based console interface. This allows the user to interact with the agents via the terminal.

```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/local/main_console.py [ln:1-12] !}
```

- **Explanation**: Here, we set up the **ConsoleUI** as the user interface for the workflow, which will allow the entire agent interaction to take place within the terminal.


### Complete Application Code

<details>
<summary>workflow.py</summary>
```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/workflow.py !}
```
</details>

<details>
<summary>main.py</summary>
```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/local/main_console.py !}
```
</details>

### Running the Application

Once the workflow is set up, you can run the application using the **FastAgency CLI**. Navigate to the directory where the script is located and run the following command:

```bash
fastagency run
```

This will launch the console interface, allowing you to input messages as the student and observe how the teacher agent responds.

!!! note
    Ensure that your **OpenAI API key** is set in the environment, as the agents rely on it to interact using **gpt-4o-mini**. If the API key is not correctly configured, the application may fail to retrieve LLM-powered responses.

### Output

Once you run it, FastAgency automatically detects the appropriate app to execute and runs it.

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

╭─ AutoGenWorkflows -> User [workflow_started] ────────────────────────────────╮
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
│ I can help you learn about mathematics. What subject you would like to       │
│  explore?:                                                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Enter a math topic you're interested in, such as **What is the triangle inequality?** and press Enter.

This will start the task, letting you watch the agents collaborate in real time to complete it. When the task is finished, you'll see an **output similar to the example below**

```console
╭─ AutoGenWorkflows -> User [workflow_completed] ──────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "result": "The triangle inequality states that for any triangle,           │
│ the sum of the lengths of any two sides must be greater than the             │
│ length of the third side. It can be expressed mathematically as \\(a +       │
│  b > c\\), \\(a + c > b\\), and \\(b + c > a\\). \n\nIn higher               │
│ dimensions, the triangle inequality applies to vector spaces, stating        │
│ that for any two vectors \\(\\mathbf{u}\\) and \\(\\mathbf{v}\\), the        │
│ inequality \\(\\|\\mathbf{u} + \\mathbf{v}\\| \\leq \\|\\mathbf{u}\\|        │
│ + \\|\\mathbf{v}\\|\\) holds, where \\(\\|\\cdot\\|\\) denotes the           │
│ norm of the vector. This principle helps determine the relationship          │
│ between the lengths of vectors and their sums, confirming that the           │
│ triangle inequality is a fundamental concept in both geometry and            │
│ linear algebra."                                                             │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

2024-10-15 16:36:20,047 [INFO] Workflow 'simple_learning' completed with result: The triangle inequality states that for any triangle, the sum of the lengths of any two sides must be greater than the length of the third side. It can be expressed mathematically as \(a + b > c\), \(a + c > b\), and \(b + c > a\).

In higher dimensions, the triangle inequality applies to vector spaces, stating that for any two vectors \(\mathbf{u}\) and \(\mathbf{v}\), the inequality \(\|\mathbf{u} + \mathbf{v}\| \leq \|\mathbf{u}\| + \|\mathbf{v}\|\) holds, where \(\|\cdot\|\) denotes the norm of the vector. This principle helps determine the relationship between the lengths of vectors and their sums, confirming that the triangle inequality is a fundamental concept in both geometry and linear algebra.
```


## Debugging Tips
If you encounter issues running the application, ensure that:

- The OpenAI API key is correctly set in your environment variables.
- All necessary packages are installed, especially the `fastagency[autogen]` dependencies.
- The API connection to gpt-4o-mini is functional and responds as expected.

---

By using **[ConsoleUI](../../../../api/fastagency/ui/console/ConsoleUI.md)**, developers can rapidly test and deploy multi-agent workflows in a simple, text-based environment. The flexibility of this interface makes it ideal for prototyping agent interactions before scaling them into more complex applications. You can extend this workflow or modify the agents for various use cases, such as tutoring, customer support, or information retrieval.
