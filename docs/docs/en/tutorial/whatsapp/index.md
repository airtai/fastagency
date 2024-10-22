# Web Scraping and Infobip WhatsApp API Integration

In this tutorial, we will explore how to leverage the **FastAgency** framework to create a dynamic and interactive chatbot that integrates two powerful agents:

1. **WebSurferAgent** – A web-scraping agent capable of retrieving relevant content from webpages.
2. **WhatsAppAgent** – An agent that interacts with the [Infobip WhatsApp API](https://www.infobip.com/docs/api/channels/whatsapp){target="_blank"} to send WhatsApp messages based on the user’s request.

The chat system will operate between these two agents and the user, allowing them to scrape web content and send the relevant information via WhatsApp, all within a seamless conversation. This tutorial will guide you through setting up these agents, handling user interaction, and ensuring secure API communication.

## What You’ll Learn

By the end of this tutorial, you will understand how to:

1. Integrate external APIs like [Infobip WhatsApp API](https://www.infobip.com/docs/api/channels/whatsapp){target="_blank"} with FastAgency.
2. Build and register agents that autonomously scrape the web for relevant information.
3. Use **FastAgency workflows** to manage agent interactions and user input.
4. Present scraped content to the user and offer sending that content via WhatsApp.
5. Handle secure API credentials and ensure safe communication between agents.

We will walk through setting up each agent, handling API security, and creating a cohesive conversation that scrapes data, processes user input, and sends it via WhatsApp in response.

Let’s dive into creating a powerful interactive agent system with **FastAgency**!


## Installation and API Key Setup

Before we dive into building our agents, let’s go over the necessary setup. We will guide you through installing the **FastAgency** framework and obtaining the API key needed for the **Infobip WhatsApp API** integration.

### Installing FastAgency

To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```bash
pip install "fastagency[autogen,mesop,openapi]"
```

### API Key Setup
**WebSurferAgent** requires an **Bing Web Search** API key and **WhatsAppAgent** requires an API key to interact with Infobip's WhatsApp service. Follow these steps to create your API keys:

#### Create Bing Web Search API Key
To create [Bing Web Search](https://www.microsoft.com/en-us/bing/apis/pricing){target="_blank"} API key, follow the guide provided.

!!! note
    You will need to create **Microsoft Azure** Account.

#### Create Infobip Account
**Step 1**: If you don’t have a Infobip account, you’ll need to sign up:

- Go to [Infobip Portal](https://www.infobip.com/signup){target="_blank"} and create account

**Step 2**: Settings

- In the **Customize your experience** section, choose:
    1. **WhatsApp**
    2. ***Customer support***
    3. ***By using code (APIs, SDKs)***

**Step 3**: Test WhatsApp API

- After you have created the account, you will be redirected [Infobip Homepage](https://portal.infobip.com/homepage){target="_blank"}.
- Check the **Send your first message** option and send a WhatsApp message to yourself. (In this tutorial, we will only be sending messages to your own number)

If you've successfully received the message, you're all set!

Copy the **API Key** from the top-right corner and continue with the next steps.

#### Set Up Your API Keys in the Environment

To securely use the API keys in your project, you should store it in an environment variables.

You can set the API keys in your terminal as an environment variable:

=== "Linux/macOS"
    ```bash
    export WHATSAPP_API_KEY="your_whatsapp_api_key"
    export BING_API_KEY="your_bing_api_key"
    ```
=== "Windows"
    ```bash
    set WHATSAPP_API_KEY="your_whatsapp_api_key"
    set BING_API_KEY="your_bing_api_key"
    ```

## Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/tutorial/whatsapp/main.py !}
```
</details>


## Code Walkthrough

Now we will go over each key part of the code, explaining its function and purpose within the FastAgency framework. Understanding these components is crucial for building a dynamic interaction between the user, the **WebSurferAgent**, and the **WhatsAppAgent**.

### Creating the WhatsApp API Instance
The following lines shows hot to initializes the WhatsApp API by loading the OpenAPI specification from a URL. The OpenAPI spec defines how to interact with the WhatsApp API, including endpoints, parameters, and security details.

Also, we configure the **WhatsApp API** with the __*WHATSAPP_API_KEY*__ using __*set_security_params*__ to authenticate our requests.
```python
{! docs_src/tutorial/whatsapp/main.py [ln:24-31] !}
```

For more information, visit [**API Integration User Guide**](../../user-guide/api){target="_blank"}.


### Registering the Workflow

Here, we initialize a new workflow using ***AutoGenWorkflows()*** and register it under the name ***"whatsapp_and_websurfer"***. The ***@wf.register*** decorator registers the function to handle chat flow with security enabled, combining both WhatsAppAgent and WebSurferAgent.

```python
{! docs_src/tutorial/whatsapp/main.py [ln:58-60] !}
```

### Interaction with the user
This is a core function used by the **WhatsAppAgent** to either present the task result or ask a follow-up question to the user. The message is wrapped in a ***TextInput*** object, and then ***ui.process_message()*** sends it for user interaction.

```python
{! docs_src/tutorial/whatsapp/main.py [ln:63-73] !}
```

### Creating the WhatsApp and WebSurfer Agents

- **WhatsAppAgent**: A ***ConversableAgent*** is created with the name "WhatsApp_Agent". It uses the system message defined earlier and relies on the termination function to end the chat when needed.
- **WebSurferAgent**: The ***WebSurferAgent*** is responsible for scraping web content and passes the retrieved data to the **WhatsAppAgent**. It’s configured with a summarizer to condense web content, which is useful when presenting concise data to the user. For more information, visit [**WebSurfer User Guide**](../../user-guide/runtimes/autogen/websurfer){target="_blank"}.

```python
{! docs_src/tutorial/whatsapp/main.py [ln:75-90] !}
```


### Registering Functions

The function ***present_completed_task_or_ask_question*** is registered to allow the **WhatsAppAgent** to ask questions or present completed tasks after receiving data from the **WebSurferAgent**.

```python
{! docs_src/tutorial/whatsapp/main.py [ln:92-99] !}
```


We register the WhatsApp API, which allows the **WhatsAppAgent** to handle tasks like suggesting messages that will be sent to the user.
```python
{! docs_src/tutorial/whatsapp/main.py [ln:101-105] !}
```

### Initiating the Chat

We initiate the conversation between the user, **WebSurferAgent**, and **WhatsAppAgent**. The user’s initial message is provided, and the system is configured to handle up to 10 turns of interaction. The conversation is summarized using the ***reflection_with_llm*** method, which uses a language model to summarize the chat.

Once the conversation ends, the summary is returned to the user, wrapping up the session.

```python
{! docs_src/tutorial/whatsapp/main.py [ln:113-120] !}
```

### Starting the Application

The FastAgency app is created, using the registered workflows (***wf***) and web-based user interface (***MesopUI***). This makes the conversation between agents and the user interactive.

```python
{! docs_src/tutorial/whatsapp/main.py [ln:123] !}
```

For more information, visit [**Mesop User Guide**](../../user-guide/ui/mesop/basics){target="_blank"}.

## Running the Application

Once the workflow is set up, you can run the application using the **FastAgency CLI**.
There are two options of running a Mesop application:

1. Using [`fastagency`](../../cli/cli.md){target="_blank"} command line:

    !!! note "Terminal (using [fastagency](../../cli/cli.md){target="_blank"})"
        ```
        fastagency run
        ```

    !!! danger "Currently not working on **MacOS**"
        The above command is currently not working on **MacOS**, please use the alternative way of starting the application from below ([#362](https://github.com/airtai/fastagency/issues/362)).

2. Using [Gunicorn](https://gunicorn.org/){target="_blank"} WSGI HTTP server:

    The preferred way to run the Mesop application is using a Python WSGI HTTP server like [Gunicorn](https://gunicorn.org/){target="_blank"}. First, you need to install it using package manager such as `pip` and then run it as follows:

    !!! note "Terminal (using [Gunicorn](https://gunicorn.org/){target="_blank"})"
        ```
        pip install gunicorn
        gunicorn main:app
        ```

    !!! danger "Currently not working on **Windows**"
        The above command is currently not working on **Windows**, because gunicorn is not supported. Please use the alternative method below to start the application:
        ```
        pip install waitress
        waitress-serve --listen=0.0.0.0:8000 main:app
        ```

```console
 ╭─ Python package file structure ──╮
 │                                  │
 │  📁 docs                         │
 │  ├── 🐍 __init__.py              │
 │  └── 📁 docs_src                 │
 │      ├── 🐍 __init__.py          │
 │      └── 📁 tutorial             │
 │          ├── 🐍 __init__.py      │
 │          └── 📁 whatsapp         │
 │              ├── 🐍 __init__.py  │
 │              └── 🐍 main.py      │
 │                                  │
 ╰──────────────────────────────────╯

/home/vscode/.local/lib/python3.10/site-packages/pydantic/_internal/_config.py:341: UserWarning: Valid config keys have changed in V2:
* 'keep_untouched' has been renamed to 'ignored_types'
  warnings.warn(message, UserWarning)
2024-10-22 10:04:31,524 [INFO] Patched OpenAPIParser.parse_schema
2024-10-22 10:04:31,527 [INFO] Importing autogen.base.py
2024-10-22 10:04:32,226 [INFO] Patching static file serving in Mesop
/home/vscode/.local/lib/python3.10/site-packages/pydantic/main.py:214: UserWarning: A custom validator is returning a value other than `self`.
Returning anything other than `self` from a top level model validator isn't supported when validating via `__init__`.
See the `model_validator` docs (https://docs.pydantic.dev/latest/concepts/validators/#model-validators) for more details.
  warnings.warn(
2024-10-22 10:04:32,726 [INFO] Initializing MesopUI: <fastagency.ui.mesop.mesop.MesopUI object at 0xffffb1122cb0>
2024-10-22 10:04:32,731 [INFO] Initialized MesopUI: <fastagency.ui.mesop.mesop.MesopUI object at 0xffffb1122cb0>
2024-10-22 10:04:32,731 [INFO] Initializing FastAgency <FastAgency title=WhatsApp chat> with workflows: <fastagency.runtimes.autogen.autogen.AutoGenWorkflows object at 0xffff94c7e530> and UI: <fastagency.ui.mesop.mesop.MesopUI object at 0xffffb1122cb0>
2024-10-22 10:04:32,731 [INFO] Initialized FastAgency: <FastAgency title=WhatsApp chat>

 ╭────────────── Importable FastAgency app ───────────────╮
 │                                                        │
 │  from docs.docs_src.tutorial.whatsapp.main import app  │
 │                                                        │
 ╰────────────────────────────────────────────────────────╯

2024-10-22 10:04:32,755 [INFO] Creating MesopUI with import string: docs.docs_src.tutorial.whatsapp.main:app
2024-10-22 10:04:32,755 [INFO] Starting MesopUI: import_string=docs.docs_src.tutorial.whatsapp.main:app, main_path=/tmp/tmp6jdunoni/main.py
2024-10-22 10:04:32,757 [INFO] Configuring static file serving with patched method
Running with hot reload:

Running server on: http://localhost:32123
 * Serving Flask app 'mesop.server.server'
 * Debug mode: off
```

The command will launch a web interface where users can input their requests and interact with the agents (in this case ***http://localhost:32123***)

!!! note
    Ensure that your OpenAI API key is set in the environment, as the agents rely on it to interact using GPT-4o. If the API key is not correctly configured, the application may fail to retrieve LLM-powered responses.

## Chat Example
In this scenario, the user instructs the agents to scrape [BBC Sport](https://www.bbc.com/sport) for the latest sports news.

![Initial message](./images/initial_message.png)

Upon receiving the request, **WebSurferAgent** initiates the process by scraping the webpage for relevant updates.

![Scraping](./images/scraping.png)

After the scraping process is complete, the agents compile the findings and present them to the user. In the final step, the user submits their phone number to receive the results via WhatsApp message.

![Scraped Info](./images/scraped_info.png)

![WhatsApp API call](./images/whatsapp_api_call.png)


Finally, the results are delivered to the user through a WhatsApp message.

![WhatsApp Message](./images/whatsapp.png)


## Conclusion

In conclusion, integrating **FastAgency** with the **Infobip WhatsApp API** offers a powerful way to build dynamic chat systems capable of scraping web data and delivering it directly to users via WhatsApp. By leveraging two agents—**WebSurferAgent** for retrieving web content and **WhatsAppAgent** for seamless messaging—you can create interactive and responsive experiences for users. This tutorial walked you through the key steps for setting up these agents, configuring API security, and handling user interaction. With this setup, you can expand your chatbot’s functionality, enabling real-time data delivery and efficient communication across platforms.
