# WhatsApp agent

FastAgency allows you to quickly create workflows with [WhatsApp](https://www.whatsapp.com/){target="_blank"} communication abilities, making it easy to integrate message sending.

## Adding WhatsApp Capabilities to Agents

FastAgency provides two ways to add [WhatsApp](https://www.whatsapp.com/){target="_blank"} communication capabilities to agents. You can either:

1. Use a [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md), which comes with built-in WhatsApp message sending capabilities (recommended)
2. Enhance an existing agent with WhatsApp capability using [**`WhatsAppTool`**](../../../api/fastagency/runtimes/ag2/tools/whatsapp/WhatsAppTool.md)

In this guide, we'll demonstrate both methods with a real-world example. We’ll create a workflow where a [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md) will help you send messages to your phone over WhatsApp.

We’ll build agents and assign them the task: “Send 'Hi!' to *YOUR_NUMBER*” to showcase its ability to interact with [Infobip WhatsApp API](https://www.infobip.com/docs/whatsapp/api){target="_blank"}.

## Installation & Setup

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**. Before getting started, make sure you have installed FastAgency with support for the [AG2](https://docs.ag2.ai/){target="_blank"} runtime by running the following command:

```bash
pip install "fastagency[autogen]"
```

This command installs FastAgency with support for the Console interface and [AG2](https://docs.ag2.ai/){target="_blank"} framework.

### Creating your WhatsApp API key

{! docs/en/snippets/creating_whatsapp_api_key.md !}

#### Set Up Your API Key in the Environment

You can set the WhatsApp API key in your terminal as an environment variable:

=== "Linux/macOS"
    ```bash
    export WHATSAPP_API_KEY="your_whatsapp_api_key"
    ```
=== "Windows"
    ```bash
    set WHATSAPP_API_KEY="your_whatsapp_api_key"
    ```

## Example: Create a workflow that will send a WhatsApp message to your phone

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
The example starts by importing the necessary modules from **AG2** and **FastAgency**. These imports lay the foundation for building and running multi-agent workflows.

=== "Using WhatsAppAgent"
    ```
    {!> docs_src/user_guide/runtimes/ag2/whatsapp.py [ln:1-9] !}
    ```

    To create a [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md), simply import [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md), which comes with built-in WhatsApp capabilities, and use it as needed.

=== "Enhancing an existing agent"
    ```
    {!> docs_src/user_guide/runtimes/ag2/whatsapp_tool.py [ln:1-10] !}
    ```

    To enhance existing agents with WhatsApp communication capability, import [**`WhatsAppTool`**](../../../api/fastagency/runtimes/ag2/tools/whatsapp/WhatsAppTool.md) from FastAgency and [**`ConversableAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/ConversableAgent){target="_blank"} from [AG2](https://docs.ag2.ai/){target="_blank"}.

#### 2. **Configure the Language Model (LLM)**
Here, the large language model is configured to use the `gpt-4o` model, and the API key is retrieved from the environment. This setup ensures that both the user and [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md) can interact effectively.

```python
{! docs_src/user_guide/runtimes/ag2/whatsapp.py [ln:11-19] !}
```

#### 3. **Define the Workflow and Agents**

=== "Using WhatsAppAgent"

    In this step, we are going to create two agents and specify the initial message that will be displayed to users when the workflow starts:

    - [**`UserProxyAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/UserProxyAgent){target="_blank"}: This agent simulates the user interacting with the system.

    - [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md): This agent has built-in capability to communicate with [Infobip WhatsApp API](https://www.infobip.com/docs/whatsapp/api){target="_blank"}.

    ```python
    {!> docs_src/user_guide/runtimes/ag2/whatsapp.py [ln:34-52] !}
    ```

    When initiating the [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md), the executor parameter must be provided. This can be either a single instance of [**`ConversableAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/ConversableAgent){target="_blank"} or a `list of `[**`ConversableAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/ConversableAgent){target="_blank"} instances.

    The [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md) relies on the executor agent(s) to execute the sending of WhatsApp messages. In this example, the `whatsapp_agent` agent will call the `user_agent` agent with the necessary instructions when contacting the WhatsApp API required, and the `user_agent` will execute those instructions.

=== "Enhancing an existing agent"

    In this step, we create two agents, a WhatsApp tool and set an initial message that will be displayed to users when the workflow starts:

    - [**`UserProxyAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/UserProxyAgent){target="_blank"}: This agent simulates the user interacting with the system.

    - [**`ConversableAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/ConversableAgent){target="_blank"}: This is the conversable agent to which we will be adding WhatsApp capabilities.

    - [**`WhatsAppTool`**](../../../api/fastagency/runtimes/ag2/tools/whatsapp/WhatsAppTool.md): The tool that gives the [**`ConversableAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/ConversableAgent){target="_blank"} the ability to interact with WhatsApp.

    ```python
    {!> docs_src/user_guide/runtimes/ag2/whatsapp_tool.py [ln:36-53] !}
    ```

    Now, we need to register the [**`WhatsAppTool`**](../../../api/fastagency/runtimes/ag2/tools/whatsapp/WhatsAppTool.md) with a caller and executor. This setup allows the caller to use the [**`WhatsAppTool`**](../../../api/fastagency/runtimes/ag2/tools/whatsapp/WhatsAppTool.md) for performing real-time WhatsApp interactions.

    ```python
    {!> docs_src/user_guide/runtimes/ag2/whatsapp_tool.py [ln:55-58] !}
    ```

    The `executor` can be either a single instance of [**`ConversableAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/ConversableAgent){target="_blank"} or a `list of `[**`ConversableAgent`**](https://docs.ag2.ai/docs/api-reference/autogen/ConversableAgent){target="_blank"} instances.

    The `caller` relies on the executor agent(s) to execute the WhatsApp tasks. In this example, the `assistant_agent` agent will call the `user_agent` agent with the necessary instructions when WhatsApp interaction is required, and the `user_agent` will execute those instructions.

#### 4. **Enable Agent Interaction and Chat**
Here, the user agent starts a conversation with the [**`WhatsAppAgent`**](../../../api/fastagency/runtimes/ag2/agents/whatsapp/WhatsAppAgent.md), which will send a message to the specified number. The conversation is then summarized using a method provided by the LLM.

=== "Using WhatsAppAgent"

    ```python
{! docs_src/user_guide/runtimes/ag2/whatsapp.py [ln:54-61] !}
    ```

=== "Enhancing an existing agent"

    ```python
{! docs_src/user_guide/runtimes/ag2/whatsapp_tool.py [ln:60-67] !}
    ```

#### 5. **Create and Run the Application**
Finally, we create the FastAgency application and launch it using the console interface.

```python
{! docs_src/user_guide/runtimes/ag2/whatsapp.py [ln:64] !}
```

### Complete Application Code

=== "Using WhatsAppAgent"

    <details>
        <summary>whatsapp_agent.py</summary>
        ```python
        {!> docs_src/user_guide/runtimes/ag2/whatsapp.py !}
        ```
    </details>

=== "Enhancing an existing agent"

    <details>
        <summary>whatsapp_tool.py</summary>
        ```python
        {!> docs_src/user_guide/runtimes/ag2/whatsapp_tool.py !}
        ```
    </details>


### Running the Application


=== "Using WhatsAppAgent"

    ```bash
    fastagency run whatsapp_agent.py
    ```

=== "Enhancing an existing agent"

    ```bash
    fastagency run whatsapp_tool.py
    ```

Ensure you have set your OpenAI API key in the environment. The command will launch a console interface where users can input their requests and interact with the whatsapp agent.

### Output

Once you run it, FastAgency automatically detects the appropriate app to execute and runs it. The application will then prompt you with: "I can help you with sending a message over whatsapp, what would you like to send?"

=== "Using WhatsAppAgent"

    ```console
    ╭─── Python package file structure ────╮
    │                                      │
    │  📁 docs                             │
    │  ├── 🐍 __init__.py                  │
    │  └── 📁 docs_src                     │
    │      ├── 🐍 __init__.py              │
    │      └── 📁 user_guide               │
    │          ├── 🐍 __init__.py          │
    │          └── 📁 runtimes             │
    │              ├── 🐍 __init__.py      │
    │              └── 📁 autogen          │
    │                  ├── 🐍 __init__.py  │
    │                  └── 🐍 whatsapp.py  │
    │                                      │
    ╰──────────────────────────────────────╯

    2024-11-06 12:05:31,205 [INFO] Importing autogen.base.py
    /home/vscode/.local/lib/python3.10/site-packages/pydantic/_internal/_config.py:341: UserWarning: Valid config keys have changed in V2:
    * 'keep_untouched' has been renamed to 'ignored_types'
    warnings.warn(message, UserWarning)
    2024-11-06 12:05:31,512 [INFO] Patched OpenAPIParser.parse_schema
    2024-11-06 12:05:31,512 [INFO] Patched Operation.function_name
    2024-11-06 12:05:31,512 [INFO] Patched fastapi_code_generator.__main__.generate_code
    2024-11-06 12:05:31,512 [INFO] Patched Parser.__apply_discriminator_type,
    2024-11-06 12:05:31,712 [INFO] Initializing FastAgency <FastAgency title=FastAgency application> with workflows: <fastagency.runtimes.ag2.ag2.AutoGenWorkflows object at 0xffffafd51810> and UI: <fastagency.ui.console.console.ConsoleUI object at 0xffffa043ccd0>
    2024-11-06 12:05:31,712 [INFO] Initialized FastAgency: <FastAgency title=FastAgency application>

    ╭───────────────────── Importable FastAgency app ──────────────────────╮
    │                                                                      │
    │  from docs.docs_src.user_guide.runtimes.ag2.whatsapp import app  │
    │                                                                      │
    ╰──────────────────────────────────────────────────────────────────────╯

    ╭─ AutoGenWorkflows -> User [workflow_started] ────────────────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "name": "simple_whatsapp",                                                 │
    │   "description": "WhatsApp chat",                                            │
    │                                                                              │
    │ "params": {}                                                                 │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you with sending a message over whatsapp, what would you          │
    │ like to send?:                                                               │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

=== "Enhancing an existing agent"

    ```console
    ╭────── Python package file structure ──────╮
    │                                           │
    │  📁 docs                                  │
    │  ├── 🐍 __init__.py                       │
    │  └── 📁 docs_src                          │
    │      ├── 🐍 __init__.py                   │
    │      └── 📁 user_guide                    │
    │          ├── 🐍 __init__.py               │
    │          └── 📁 runtimes                  │
    │              ├── 🐍 __init__.py           │
    │              └── 📁 autogen               │
    │                  ├── 🐍 __init__.py       │
    │                  └── 🐍 whatsapp_tool.py  │
    │                                           │
    ╰───────────────────────────────────────────╯

    2024-11-06 12:01:55,921 [INFO] Importing autogen.base.py
    /home/vscode/.local/lib/python3.10/site-packages/pydantic/_internal/_config.py:341: UserWarning: Valid config keys have changed in V2:
    * 'keep_untouched' has been renamed to 'ignored_types'
    warnings.warn(message, UserWarning)
    2024-11-06 12:01:56,374 [INFO] Patched OpenAPIParser.parse_schema
    2024-11-06 12:01:56,374 [INFO] Patched Operation.function_name
    2024-11-06 12:01:56,374 [INFO] Patched fastapi_code_generator.__main__.generate_code
    2024-11-06 12:01:56,374 [INFO] Patched Parser.__apply_discriminator_type,
    2024-11-06 12:01:56,611 [INFO] Initializing FastAgency <FastAgency title=FastAgency application> with workflows: <fastagency.runtimes.ag2.ag2.AutoGenWorkflows object at 0xffff88721840> and UI: <fastagency.ui.console.console.ConsoleUI object at 0xffff89e50760>
    2024-11-06 12:01:56,611 [INFO] Initialized FastAgency: <FastAgency title=FastAgency application>

    ╭──────────────────────── Importable FastAgency app ────────────────────────╮
    │                                                                           │
    │  from docs.docs_src.user_guide.runtimes.ag2.whatsapp_tool import app  │
    │                                                                           │
    ╰───────────────────────────────────────────────────────────────────────────╯

    ╭─ AutoGenWorkflows -> User [workflow_started] ────────────────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "name": "simple_whatsapp",                                                 │
    │   "description": "WhatsApp chat",                                            │
    │                                                                              │
    │ "params": {}                                                                 │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you with sending a message over whatsapp, what would you          │
    │ like to send?:                                                               │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

In the prompt, type **Send "Hi!" to *YOUR-NUMBER*** and press Enter.

This will initiate the task, allowing you to see the real-time conversation between the agents as they collaborate to complete it. Once the task is finished, you’ll see an output similar to the one below.

```console
╭─ User_Agent -> Assistant_Agent [text_message] ───────────────────────────────╮
│                                                                              │
│ Send "Hi!" to 123456789                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Assistant_Agent -> User_Agent [suggested_function_call] ────────────────────╮
│                                                                              │
│ {                                                                            │
│   "function_name": "send_whatsapp_text_message",                             │
│   "call_id":                                                                 │
│ "call_NnptdiOOvZNjzHPb7grxwr9d",                                             │
│   "arguments": {                                                             │
│     "body": {                                                                │
│                                                                              │
│ "from": "447860099299",                                                      │
│       "to": "123456789",                                                     │
│       "messageId":                                                           │
│  "test-message-12345",                                                       │
│       "content": {                                                           │
│         "text": "Hi!"                                                        │
│                                                                              │
│ },                                                                           │
│       "callbackData": "User_Agent"                                           │
│     }                                                                        │
│   }                                                                          │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ User_Agent -> Assistant_Agent [function_call_execution] ────────────────────╮
│                                                                              │
│ {                                                                            │
│   "function_name": "send_whatsapp_text_message",                             │
│   "call_id":                                                                 │
│ "call_NnptdiOOvZNjzHPb7grxwr9d",                                             │
│   "retval": "{\"to\":                                                        │
│ \"123456789\", \"messageCount\": 1, \"messageId\": \"test-                   │
│ message-12345\", \"status\": {\"groupId\": 1, \"groupName\":                 │
│ \"PENDING\", \"id\": 7, \"name\": \"PENDING_ENROUTE\",                       │
│ \"description\": \"Message sent to next instance\"}}\n"                      │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Assistant_Agent -> User_Agent [text_message] ───────────────────────────────╮
│                                                                              │
│ The message "Hi!" has been sent to 123456789. The current status of          │
│  the message is "PENDING."                                                   │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ User_Agent -> Assistant_Agent [text_message] ───────────────────────────────╮
│                                                                              │
│ TERMINATE                                                                    │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ AutoGenWorkflows -> User [workflow_completed] ──────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "result": "The message \"Hi!\" was successfully sent to the number         │
│  123456789, and its status is currently \"PENDING.\""                        │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

If you configured your WHATSAPP_API_KEY correctly, you should get a message from your agent to your WhatsApp now.

---

This example highlights the capabilities of the [AG2](https://docs.ag2.ai/){target="_blank"} runtime within FastAgency, demonstrating how seamlessly LLM-powered agents can be integrated with [WhatsApp](https://www.whatsapp.com/){target="_blank"} for real-time, automated messaging. By using FastAgency, developers can rapidly build interactive, scalable applications that connect with external APIs—such as those for [WhatsApp](https://www.whatsapp.com/){target="_blank"} messaging, CRM systems, or custom data services—enabling the retrieval and delivery of dynamic content directly through [WhatsApp](https://www.whatsapp.com/){target="_blank"}. This setup empowers users to automate communication workflows, integrate live data, and facilitate on-demand, personalized interactions with end users.
