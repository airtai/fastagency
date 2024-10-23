# Web Scraping and Giphy API Integration

In this tutorial, we will explore how to leverage the **FastAgency** framework to create a dynamic and interactive chatbot that integrates two powerful agents:

**WebSurferAgent** – A web-scraping agent capable of retrieving relevant content from webpages.
**GiphyAgent** – An agent that interacts with the [Giphy](https://giphy.com){target="_blank"} **API** to fetch GIFs based on the user’s request.

The chat system will operate between these two agents and the user, allowing them to scrape web content and generate GIFs based on that content, all within a seamless conversation. This tutorial will guide you through setting up these agents and handling user interaction in a secure, structured, and intuitive manner.

## What You’ll Learn

By the end of this tutorial, you’ll understand how to:

- Integrate external APIs like [Giphy](https://giphy.com){target="_blank"} with **FastAgency**.
- Build and register agents that can autonomously scrape the web for relevant information.
- Use **FastAgency** workflows to manage agent interactions and user input.
- Present scraped content to the user and offer personalized GIF suggestions based on that content.

We will walk through setting up each agent, handling API security, and creating a cohesive conversation that can scrape data, process user input, and generate GIFs in response.

Let’s dive into creating a powerful interactive agent system with **FastAgency**!


## Installation and API Key Setup

Before we dive into building our agents, let’s go over the necessary setup. We will guide you through installing the **FastAgency** framework and obtaining the API key needed for the Giphy integration.

### Installing FastAgency

To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```bash
pip install "fastagency[autogen,mesop,openapi]"
```

### API Key Setup
**WebSurferAgent** requires an **Bing Web Search** API key and **GiphyAgent** requires an API key to interact with Giphy's service. Follow these steps to create your API keys:

#### Create Bing Web Search API Key
To create [Bing Web Search](https://www.microsoft.com/en-us/bing/apis/pricing){target="_blank"} API key, follow the guide provided.

!!! note
    You will need to create **Microsoft Azure** Account.

#### Create a Giphy Account
**Step 1**: If you don’t have a Giphy account, you’ll need to sign up:

- Go to [Giphy Developers](https://developers.giphy.com){target="_blank"}
- Click on **Create Account**.

**Step 2**: Navigate to [Dashboard](https://developers.giphy.com/dashboard/){target="_blank"}
!!! note
    You may need to wait a few minutes after creating your account before being able to access the **Dashboard** page.
- Click on **Create an API key** and choose **API** as the type of app and give it a name (e.g., "FastAgency Giphy App").
- Agree to the terms and click Create App.

**Step 3**: Get Your API Key
After creating the app, you’ll be provided with an **API Key**.

- Copy this key and continue with the following steps.

#### Set Up Your API Keys in the Environment

To securely use the API keys in your project, you should store it in an environment variables.

You can set the API keys in your terminal as an environment variable:

=== "Linux/macOS"
    ```bash
    export GIPHY_API_KEY="your_giphy_api_key"
    export BING_API_KEY="your_bing_api_key"
    ```
=== "Windows"
    ```bash
    set GIPHY_API_KEY="your_giphy_api_key"
    set BING_API_KEY="your_bing_api_key"
    ```

## Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/tutorial/giphy/main.py !}
```
</details>


## Code Walkthrough

Now we will go over each key part of the code, explaining its function and purpose within the FastAgency framework. Understanding these components is crucial for building a dynamic interaction between the user, the **WebSurferAgent**, and the **GiphyAgent**.

### Creating the Giphy API Instance
The following lines shows hot to initializes the Giphy API by loading the OpenAPI specification from a URL. The OpenAPI spec defines how to interact with the Giphy API, including endpoints, parameters, and security details.

Also, we configure the **Giphy API** with the __*GIPHY_API_KEY*__ using __*set_security_params*__ to authenticate our requests.
```python
{! docs_src/tutorial/giphy/main.py [ln:25-29] !}
```

For more information, visit [**API Integration User Guide**](../../user-guide/api/index.md){target="_blank"}.

### Registering the Workflow

Here, we initialize a new workflow using ***AutoGenWorkflows()*** and register it under the name ***"giphy_and_websurfer"***. The ***@wf.register*** decorator registers the function to handle chat flow with security enabled, combining both GiphyAgent and WebSurferAgent.

```python
{! docs_src/tutorial/giphy/main.py [ln:58-61] !}
```

### Interaction with the user
This is a core function used by the **GiphyAgent** to either present the task result or ask a follow-up question to the user. The message is wrapped in a ***TextInput*** object, and then ***ui.process_message()*** sends it for user interaction.

```python
{! docs_src/tutorial/giphy/main.py [ln:65-76] !}
```

### Creating the Giphy and WebSurfer Agents

- **GiphyAgent**: A ***ConversableAgent*** is created with the name "Giphy_Agent". It uses the system message defined earlier and relies on the termination function to end the chat when needed.
- **WebSurferAgent**: The ***WebSurferAgent*** is responsible for scraping web content and passes the retrieved data to the **GiphyAgent**. It’s configured with a summarizer to condense web content, which is useful when presenting concise data to the user. For more information, visit [**WebSurfer User Guide**](../../user-guide/runtimes/autogen/websurfer.md){target="_blank"}.

```python
{! docs_src/tutorial/giphy/main.py [ln:77-92] !}
```

### Registering Functions

The function ***present_completed_task_or_ask_question*** is registered to allow the **GiphyAgent** to ask questions or present completed tasks after receiving data from the **WebSurferAgent**.

```python
{! docs_src/tutorial/giphy/main.py [ln:94-101] !}
```

We specify which Giphy API functions can be used by the **GiphyAgent**: *random_gif*, *search_gifs*, and *trending_gifs*. These functions allow the agent to generate GIFs based on user input or trending content.
```python
{! docs_src/tutorial/giphy/main.py [ln:103-109] !}
```

### Initiating the Chat

We initiate the conversation between the user, **WebSurferAgent**, and **GiphyAgent**. The user’s initial message is provided, and the system is configured to handle up to 10 turns of interaction. The conversation is summarized using the ***reflection_with_llm*** method, which uses a language model to summarize the chat.

Once the conversation ends, the summary is returned to the user, wrapping up the session.

```python
{! docs_src/tutorial/giphy/main.py [ln:117-124] !}
```

### Starting the Application

The FastAgency app is created, using the registered workflows (***wf***) and web-based user interface (***MesopUI***). This makes the conversation between agents and the user interactive.

```python
{! docs_src/tutorial/giphy/main.py [ln:127] !}
```

For more information, visit [**Mesop User Guide**](../../user-guide/ui/mesop/basics.md){target="_blank"}.

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
 │          └── 📁 giphy            │
 │              ├── 🐍 __init__.py  │
 │              └── 🐍 main.py      │
 │                                  │
 ╰──────────────────────────────────╯

/home/vscode/.local/lib/python3.10/site-packages/pydantic/_internal/_config.py:341: UserWarning: Valid config keys have changed in V2:
* 'keep_untouched' has been renamed to 'ignored_types'
  warnings.warn(message, UserWarning)
 [INFO] Importing autogen.base.py
/home/vscode/.local/lib/python3.10/site-packages/pydantic/main.py:214: UserWarning: A custom validator is returning a value other than `self`.
Returning anything other than `self` from a top level model validator isn't supported when validating via `__init__`.
See the `model_validator` docs (https://docs.pydantic.dev/latest/concepts/validators/#model-validators) for more details.
  warnings.warn(

 ╭───────────── Importable FastAgency app ─────────────╮
 │                                                     │
 │  from docs.docs_src.tutorial.giphy.main import app  │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

 [INFO] Creating MesopUI with import string: docs.docs_src.tutorial.giphy.main:app
 [INFO] Starting MesopUI: import_string=docs.docs_src.tutorial.giphy.main:app, main_path=/tmp/tmpfi8uxdgv/main.py
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

![Scraping 1](./images/scraping1.png)

![Scraping 2](./images/scraping2.png)

Once the scraping is complete, the agents deliver their findings to the user.
In the final step, the user asks for a few *Premier League* GIFs, which **GiphyAgent** promptly provides.

![Scraped Info](./images/scraped_info.png)

![Gifs](./images/gifs.png)

## Conclusion

In this tutorial, we walked through how to create a simple chatbot using **FastAgency** that can scrape web content and provide relevant GIFs. By integrating the **WebSurferAgent** and **GiphyAgent**, we built a tool that lets users gather information from the web and request GIFs all in one conversation.

You’ve learned how to:

- Set up and connect external APIs, like Giphy, to your project.
- Handle API key security.
- Build an interactive workflow where users can scrape content and get personalized responses.
- Offer dynamic, engaging conversations with added visuals like GIFs.
- With these skills, you now have the foundation to expand and add more features to your chatbot, making it even more interactive and useful.
