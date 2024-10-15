# Mesop

**[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI/)** in FastAgency offers a web-based interface for interacting with multi-agent workflows. Unlike the **ConsoleUI**, which is text-based and runs in the command line, MesopUI provides a user-friendly browser interface, making it ideal for applications that need a more engaging, graphical interaction. MesopUI is perfect for building interactive web applications and enabling users to interact with agents in a more intuitive way.

Below, we’ll demonstrate how to set up a basic student-teacher conversation using **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI/)**.

## Installation

To install **FastAgency** with MesopUI support, use the following command:

```bash
pip install "fastagency[autogen,mesop]"
```

This command ensures that the required dependencies for both **AutoGen** and **Mesop** are installed.

## Usage

You can simply create Mesop based UI by importing and instantiating the `MesopUI` class with no parameters:

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:9] !}

ui = MesopUI()
```

However, you might want to add some customisation to the look-and-feel of the user interface or change some security settings as follows:

### Security

You can pass a custom [SecurityPolicy](https://google.github.io/mesop/api/page/#mesop.security.security_policy.SecurityPolicy){target="_blank"} object and specify things such as:

- a list of allowed iframe parents,

- a list of sites you can connect to,

- a list of sites you load scripts from, and

- a flag to disable trusted types.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:4] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:9] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:60] !}

ui = MesopUI(security_policy=security_policy)
```

Please see the [Mesop documentation](https://google.github.io/mesop/api/page/#mesop.security.security_policy.SecurityPolicy){target="_blank"} for details.

### Modifying styles

All [Styles](https://google.github.io/mesop/api/style/){target="_blank"} used in styling of Mesop components can be passed to the [`MesopUI`](../../../../api/fastagency/ui/mesop/MesopUI/)constructor and change the default behavior. They are specified in top-level styling class [`MesopHomePageStyles`](../../../../api/fastagency/ui/mesop/styles/MesopHomePageStyles/).

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:4] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:9] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:62-86] !}

ui = MesopUI(styles=styles)
```

## Example: Student and Teacher Learning Chat

This example shows how to create a simple learning chat where a student agent interacts with a teacher agent. The student asks questions, and the teacher provides responses, simulating a learning environment. The conversation is facilitated through the web interface using **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI/)**.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
We begin by importing the necessary modules from **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:1-14] !}
```

- **ConversableAgent**: This class allows the creation of agents that can engage in conversational tasks.
- **[FastAgency](../../../../api/fastagency/FastAgency/)**: The core class responsible for orchestrating workflows and connecting them with UIs.
- **[UI](../../../../api/fastagency/UI/)** and **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI/)**: These classes define the user interface for interaction, with **MesopUI** enabling a web-based interaction.
- **[AutoGenWorkflows](../../../../api/fastagency/runtimes/autogen/base/AutoGenWorkflows/)**: Manages the creation and execution of multi-agent workflows.

#### 2. **Configure the Language Model (LLM)**
Next, we configure the language model that powers the agents. In this case, we're using **GPT-4o**, and the API key is retrieved from the environment.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:16-24] !}
```

- **Explanation**: The configuration specifies the LLM model and API key used for powering the conversation between agents. The temperature is set to `0.0` to ensure deterministic responses from the agents, making interactions consistent and reliable.

#### 3. **Define the Workflow and Agents**
Here, we define a simple workflow where the **Student Agent** interacts with the **Teacher Agent**. The student asks questions, and the teacher responds as a math teacher. The workflow is registered using **AutoGenWorkflows**.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:26-58] !}
```

- **Agent Overview**: The **Student Agent** is configured with a system message, "You are a student willing to learn," and will initiate questions during the interaction. The **Teacher Agent**, on the other hand, is set up as a math teacher and will respond to the student's questions.
- **Workflow Registration**: The workflow is registered under the name `simple_learning`. The **ConversableAgent** class is used to represent both the student and teacher agents, allowing them to communicate with each other up to 5 turns before summarizing the conversation using the `reflection_with_llm` method.

#### 4. **Using MesopUI**
Finally, we instantiate **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI/)** to link the workflow to a web-based interface. This allows the user to interact with the agents through a web browser.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:59-90] !}
```

- **Explanation**: Here, we set up the **MesopUI** as the user interface for the workflow, which will allow the entire agent interaction to take place through a web-based platform.


### Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/ui/mesop/main_mesop.py !}
```
</details>


### Running the Application

There are two options of running a Mesop application:

1. Using [`fastagency`](../../../../cli/cli/) command line:

    !!! note "Terminal (using [fastagency](../../../../cli/cli/))"
        ```
        fastagency run
        ```

    !!! danger "Currently not working on **MacOS**"
        The above command is currently not working on **MacOS**, please use the alternative way of starting the application from below ([#362](https://github.com/airtai/fastagency/issues/362){target="_blank"}).

2. Using [Gunicorn](https://gunicorn.org/){target="_blank"} WSGI HTTP server:

    The preferred way to run the Mesop application is using a Python WSGI HTTP server like [Gunicorn](https://gunicorn.org/){target="_blank"}. First, you need to install it using package manager such as `pip` and then run it as follows:

    !!! note "Terminal (using [Gunicorn](https://gunicorn.org/){target="_blank"})"
        ```
        pip install gunicorn
        gunicorn main:app
        ```

---

!!! note
    Ensure that your OpenAI API key is set in the environment, as the agents rely on it to interact using **gpt-4o-mini**. If the API key is not correctly configured, the application may fail to retrieve LLM-powered responses.

### Output

The outputs will vary based on the interface, here is the output of the last terminal starting UI:

```console
[2024-10-15 16:57:44 +0530] [36365] [INFO] Starting gunicorn 23.0.0
[2024-10-15 16:57:44 +0530] [36365] [INFO] Listening at: http://127.0.0.1:8000 (36365)
[2024-10-15 16:57:44 +0530] [36365] [INFO] Using worker: sync
[2024-10-15 16:57:44 +0530] [36366] [INFO] Booting worker with pid: 36366
```
![Initial message](../../../getting-started/images/chat.png)

## Debugging Tips
If you encounter issues running the application, ensure that:

- The OpenAI API key is correctly set in your environment variables.
- All necessary packages are installed, especially the `fastagency[autogen,mesop]` dependencies.
- The MesopUI web interface is accessible from the browser, and no firewall is blocking the connection.

---

By using **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI/)**, developers can create interactive, web-based multi-agent applications with ease. This interface is ideal for building user-friendly, browser-accessible systems, enabling users to interact with agents in a more engaging and visual environment. You can extend this workflow for more complex scenarios, such as tutoring systems, customer support, or real-time information retrieval.
