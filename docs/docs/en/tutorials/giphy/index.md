# Web Scraping and Giphy API Integration

In this tutorial, we will explore how to leverage the **FastAgency** framework to create a dynamic and interactive chatbot that integrates two powerful agents:

1. [**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md) – A web-scraping agent capable of retrieving relevant content from webpages (learn more [here](../../user-guide/runtimes/ag2/websurfer.md)).

2. **Giphy agent** – An agent that interacts with the [Giphy](https://giphy.com){target="_blank"} API to fetch GIFs based on the user’s request. It will be created using the standard [**`ConversableAgent`**](https://docs.ag2.ai/latest/docs/api-reference/autogen/ConversableAgent/){target="_blank"} from [AG2](https://docs.ag2.ai/){target="_blank"} and the [**`OpenAPI`**](../../api/fastagency/api/openapi/OpenAPI.md) object instantiated with an OpenAPI [specification](https://raw.githubusercontent.com/ag2ai/fastagency/refs/heads/main/examples/openapi/giphy_openapi.json){target="_blank"}

The chat system will operate between these two agents and the user, allowing them to scrape web content and generate GIFs based on that content, all within a seamless conversation. This tutorial will guide you through setting up these agents and handling user interaction in a secure, structured, and intuitive manner.

## What You’ll Learn

By the end of this tutorial, you’ll understand how to:

1. Integrate external APIs like [Giphy](https://giphy.com){target="_blank"} with **FastAgency**.
2. Build and register agents that autonomously scrape the web for relevant information using [**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md).
3. Use [**`Workflow`**](../../api/fastagency/runtimes/ag2/Workflow.md) to manage agent interactions and user input.
4. Present scraped content to the user and offer personalized GIF suggestions based on that content.

We will walk through setting up each agent, handling API security, and creating a cohesive conversation that can scrape data, process user input, and generate GIFs in response.

Let’s dive into creating a powerful interactive agent system with **FastAgency**!


## Project setup

{! docs/en/tutorials/mesop_template.md[ln:3-105] !}


### API Key Setup
[**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md) requires an **Bing Web Search** API key and **Giphy agent** requires an API key to interact with Giphy's service. Follow these steps to create your API keys:

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

### Workflow Code
{! docs/en/tutorials/mesop_template.md[ln:108-112] !}

<details>
<summary>workflow.py</summary>
```python
{! docs_src/tutorials/giphy/main.py !}
```
</details>

### Deployment Code
{! docs/en/tutorials/mesop_template.md[ln:116-127] !}



## Code Walkthrough

Now we will go over each key part of the code, explaining its function and purpose within the FastAgency framework. Understanding these components is crucial for building a dynamic interaction between the user, the [**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md), and the **Giphy agent**.

### Creating the Giphy API Instance
The following lines shows hot to initializes the Giphy API by loading the OpenAPI specification from a URL. The OpenAPI spec defines how to interact with the Giphy API, including endpoints, parameters, and security details.

Also, we configure the **Giphy API** with the __*GIPHY_API_KEY*__ using __*set_security_params*__ to authenticate our requests.
```python
{! docs_src/tutorials/giphy/main.py [ln:23-27] !}
```

For more information, visit [**API Integration User Guide**](../../user-guide/api/index.md){target="_blank"}.

### Registering the Workflow

Here, we initialize a new workflow using ***Workflow()*** and register it under the name ***"giphy_and_websurfer"***. The ***@wf.register*** decorator registers the function to handle chat flow with security enabled, combining both Giphy agent and WebSurferAgent.

```python
{! docs_src/tutorials/giphy/main.py [ln:56-59] !}
```

### Interaction with the user
This is a core function used by the **Giphy agent** to either present the task result or ask a follow-up question to the user. The message is wrapped in a ***TextInput*** object, and then ***ui.process_message()*** sends it for user interaction.

```python
{! docs_src/tutorials/giphy/main.py [ln:63-73] !}
```

### Creating the Giphy and WebSurfer Agents

- **Giphy agent**: A ***ConversableAgent*** is created with the name "Giphy_Agent". It uses the system message defined earlier and relies on the termination function to end the chat when needed.
- **WebSurferAgent**: The *[**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md)* is responsible for scraping web content and passes the retrieved data to the **Giphy agent**. It’s configured with a summarizer to condense web content, which is useful when presenting concise data to the user. For more information, visit [**WebSurfer User Guide**](../../user-guide/runtimes/ag2/websurfer.md){target="_blank"}.

```python
{! docs_src/tutorials/giphy/main.py [ln:75-90] !}
```

### Registering Functions

The function ***present_completed_task_or_ask_question*** is registered to allow the **Giphy agent** to ask questions or present completed tasks after receiving data from the [**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md).

```python
{! docs_src/tutorials/giphy/main.py [ln:92-99] !}
```

We specify which Giphy API functions can be used by the **Giphy agent**: *random_gif*, *search_gifs*, and *trending_gifs*. These functions allow the agent to generate GIFs based on user input or trending content.
```python
{! docs_src/tutorials/giphy/main.py [ln:101-107] !}
```

### Initiating the Chat

We initiate the conversation between the user, [**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md), and **Giphy agent**. The user’s initial message is provided, and the system is configured to handle up to 10 turns of interaction. The conversation is summarized using the ***reflection_with_llm*** method, which uses a language model to summarize the chat.

Once the conversation ends, the summary is returned to the user, wrapping up the session.

```python
{! docs_src/tutorials/giphy/main.py [ln:115-122] !}
```

### Starting the Application

{! docs/en/tutorials/mesop_template.md[ln:132-138] !}

## Running the Application

{! docs/en/tutorials/mesop_template.md[ln:143-178] !}


## Chat Example
In this scenario, the user instructs the agents to scrape [BBC Sport](https://www.bbc.com/sport) for the latest sports news.

![Initial message](./images/initial_message.png)

Upon receiving the request, [**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md) initiates the process by scraping the webpage for relevant updates.

![Scraping 1](./images/scraping1.png)

![Scraping 2](./images/scraping2.png)

Once the scraping is complete, the agents deliver their findings to the user.
In the final step, the user asks for a few *Premier League* GIFs, which **Giphy agent** promptly provides.

![Scraped Info](./images/scraped_info.png)

![Gifs](./images/gifs.png)

## Conclusion

In this tutorial, we walked through how to create a simple chatbot using **FastAgency** that can scrape web content and provide relevant GIFs. By integrating the [**`WebSurferAgent`**](../../api/fastagency/runtimes/ag2/agents/websurfer/WebSurferAgent.md) and **Giphy agent**, we built a tool that lets users gather information from the web and request GIFs all in one conversation.

You’ve learned how to:

- Set up and connect external APIs, like Giphy, to your project.
- Handle API key security.
- Build an interactive workflow where users can scrape content and get personalized responses.
- Offer dynamic, engaging conversations with added visuals like GIFs.
- With these skills, you now have the foundation to expand and add more features to your chatbot, making it even more interactive and useful.
