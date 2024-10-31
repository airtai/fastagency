# WhatsApp API Integration and Web Scraping

In this tutorial, we will explore how to leverage the **FastAgency** framework to create a dynamic and interactive chatbot that integrates two powerful agents:

1. [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md): A web-scraping agent capable of retrieving relevant content from webpages (learn more [here](../../user-guide/runtimes/autogen/websurfer.md)).

2. **WhatsApp agent** – An agent that interacts with the [Infobip WhatsApp API](https://www.infobip.com/docs/api/channels/whatsapp){target="_blank"} to send WhatsApp messages based on the user’s request. It will be created using the standard [**`ConversableAgent`**](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/){target="_blank"} from [AutoGen](https://microsoft.github.io/autogen){target="_blank"} and the [**`OpenAPI`**](../../api/fastagency/api/openapi/OpenAPI.md) object instantiated with an OpenAPI [specification](https://dev.infobip.com/openapi/products/whatsapp.json){target="_blank"} of Infobip's [REST API](https://www.infobip.com/docs/api/channels/whatsapp){target="_blank"}.

The chat system will operate between these two agents and the user, allowing them to scrape web content and send the relevant information via WhatsApp, all within a seamless conversation. This tutorial will guide you through setting up these agents, handling user interaction, and ensuring secure API communication.

## What You’ll Learn

By the end of this tutorial, you will understand how to:

1. Integrate external APIs like [Infobip WhatsApp API](https://www.infobip.com/docs/api/channels/whatsapp){target="_blank"} using [**`OpenAPI`**](../../api/fastagency/api/openapi/OpenAPI.md).
2. Build and register agents that autonomously scrape the web for relevant information using [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md).
3. Use [**`AutoGenWorkflows`**](../../api/fastagency/runtimes/autogen/AutoGenWorkflows.md) to manage agent interactions and user input.
4. Present scraped content to the user and offer sending that content via WhatsApp.
5. Handle secure API credentials and ensure safe communication between agents using [**`APIKeyHeader`**](../../api/fastagency/api/openapi/security/APIKeyHeader.md).

We will walk through setting up each agent, handling API security, and creating a cohesive conversation that scrapes data, processes user input, and sends it via WhatsApp in response.

Let’s dive into creating a powerful interactive agent system with **FastAgency**!


## Installation and API Key Setup

Before we dive into building our agents, let’s go over the necessary setup. We will guide you through installing the **FastAgency** framework and obtaining the API key needed for the **Infobip WhatsApp API** integration.

### Installing FastAgency

To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```bash
pip install "fastagency[autogen,mesop,openapi]"
```

Alternatively, you can use [**Cookiecutter**](../../user-guide/cookiecutter/index.md), which is the preferred method. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

### API Key Setup
[**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md) requires an **Bing Web Search** API key and **WhatsAppAgent** requires an API key to interact with Infobip's WhatsApp service. Follow these steps to create your API keys:

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
- Check the **Send your first message** option and send a WhatsApp message to yourself.
- In this tutorial, we will only be sending messages **to your own number**

!!! note "Important"
    Upon receiving this message, please **reply** (e.g., with "Hi") to initiate the session. Note that sessions expire after 24 hours. If your session has expired, simply send another message to create a new one.

Copy the **API Key** from the top-right corner and continue with the next steps.

**Step 4**: Register your WhatsApp sender (Optional)

- By default, Infobip number will be used as the sender for your messages.
- If you wish to create a new sender phone number and customize your branding (including your name and logo), click on [Register Sender](https://portal.infobip.com/channels-and-numbers/channels/whatsapp/senders){target="_blank"}.

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
{! docs_src/tutorials/whatsapp/main.py !}
```
</details>


## Code Walkthrough

Now we will go over each key part of the code, explaining its function and purpose within the FastAgency framework. Understanding these components is crucial for building a dynamic interaction between the user, the [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md), and the **WhatsAppAgent**.

### Creating the WhatsApp API Instance
The following lines shows how to initializes the WhatsApp API by loading the OpenAPI specification from a URL. The OpenAPI spec defines how to interact with the WhatsApp API, including endpoints, parameters, and security details.

Also, we configure the **WhatsApp API** with the __*WHATSAPP_API_KEY*__ using __*set_security_params*__ to authenticate our requests.
```python
{! docs_src/tutorials/whatsapp/main.py [ln:24-33] !}
```

For more information, visit [**API Integration User Guide**](../../user-guide/api/index.md){target="_blank"}.


### Registering the Workflow

Here, we initialize a new workflow using ***AutoGenWorkflows()*** and register it under the name ***"whatsapp_and_websurfer"***. The ***@wf.register*** decorator registers the function to handle chat flow with security enabled, combining both WhatsAppAgent and WebSurferAgent.

```python
{! docs_src/tutorials/whatsapp/main.py [ln:60-64] !}
    ...
```

### Interaction with the user
This is a core function used by the **WhatsAppAgent** to either present the task result or ask a follow-up question to the user. The message is wrapped in a ***TextInput*** object, and then ***ui.process_message()*** sends it for user interaction.

```python
{! docs_src/tutorials/whatsapp/main.py [ln:68-78] !}
```

### Creating the WhatsApp and WebSurfer Agents

- **WhatsAppAgent**: A [**`ConversableAgent`**](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/){target="_blank"} is created with the name "WhatsApp_Agent". It uses the system message defined earlier and relies on the termination function to end the chat when needed.
- [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md): The [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md) is responsible for scraping web content and passes the retrieved data to the **WhatsAppAgent**. It’s configured with a summarizer to condense web content, which is useful when presenting concise data to the user. For more information, visit [**WebSurfer User Guide**](../../user-guide/runtimes/autogen/websurfer.md).

```python
{! docs_src/tutorials/whatsapp/main.py [ln:80-96] !}
```


### Registering Functions

The function ***present_completed_task_or_ask_question*** is registered to allow the **WhatsAppAgent** to ask questions or present completed tasks after receiving data from the [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md).

```python
{! docs_src/tutorials/whatsapp/main.py [ln:98-105] !}
```


We register the WhatsApp API, which allows the **WhatsAppAgent** to handle tasks like suggesting messages that will be sent to the user.
```python
{! docs_src/tutorials/whatsapp/main.py [ln:107-112] !}
```

### Initiating the Chat

We initiate the conversation between the user, [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md), and **WhatsAppAgent**. The user’s initial message is provided, and the system is configured to handle up to 10 turns of interaction. The conversation is summarized using the ***reflection_with_llm*** method, which uses a language model to summarize the chat.

Once the conversation ends, the summary is returned to the user, wrapping up the session.

```python
{! docs_src/tutorials/whatsapp/main.py [ln:120-125] !}
```

### Starting the Application

The FastAgency app is created, using the registered workflows (**`wf`**) and web-based user interface ([**`MesopUI`**](../../api/fastagency/ui/mesop/MesopUI.md)). This makes the conversation between agents and the user interactive.

```python
{! docs_src/tutorials/whatsapp/main.py [ln:130] !}
```

For more information, visit [**Mesop User Guide**](../../user-guide/ui/mesop/basics.md){target="_blank"}.

## Running the Application

The preferred way to run the [**Mesop**](https://google.github.io/mesop/){target="_blank"} application is using a Python WSGI HTTP server like [**Gunicorn**](https://gunicorn.org/){target="_blank"} on Linux and Mac or [**Waitress**](https://docs.pylonsproject.org/projects/waitress/en/stable/){target="_blank"} on Windows.

=== "Cookiecutter"
    !!! note "Terminal"
        ```console
        gunicorn main:app
        ```
=== "env + pip"

    First, install the package using package manager such as `pip` and then run it:

    === "Linux/MacOS"
        !!! note "Terminal"
            ```console
            pip install gunicorn
            gunicorn main:app
            ```

    === "Windows"
        !!! note "Terminal"
            ```console
            pip install waitress
            waitress-serve --listen=0.0.0.0:8000 main:app
            ```

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8000 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

The command will launch a web interface where users can input their requests and interact with the agents (in this case ***http://localhost:8000***)

!!! note
    Ensure that your OpenAI API key is set in the environment, as the agents rely on it to interact using GPT-4o. If the API key is not correctly configured, the application may fail to retrieve LLM-powered responses.

## Chat Example
In this scenario, the user instructs the agents to scrape [BBC Sport](https://www.bbc.com/sport) for the latest sports news.

![Initial message](./images/initial_message.png)

Upon receiving the request, [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md) initiates the process by scraping the webpage for relevant updates.

![Scraping](./images/scraping.png)

After the scraping process is complete, the agents compile the findings and present them to the user. In the final step, the user submits their phone number to receive the results via WhatsApp message.

![Scraped Info](./images/scraped_info.png)

![WhatsApp API call](./images/whatsapp_api_call.png)


Finally, the results are delivered to the user through a WhatsApp message.

![WhatsApp Message](./images/whatsapp.png)


## Conclusion

In summary, connecting **FastAgency** with the **Infobip WhatsApp API** lets you create chat systems that can gather web data and send it straight to users on WhatsApp. By using two agents — [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md) to pull web content and **WhatsAppAgent** for messaging, you can build engaging experiences for users. This tutorial covered the essential steps to set up these agents, secure the API, and manage user interactions. With this setup, you can enhance your chatbot’s capabilities, providing real-time information and smooth communication across different platforms.
