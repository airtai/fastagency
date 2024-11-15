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

## Project setup

{! docs/en/tutorials/mesop_template.md[ln:3-105] !}


### API Key Setup
[**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md) requires an **Bing Web Search** API key and **WhatsAppAgent** requires an API key to interact with Infobip's WhatsApp service. Follow these steps to create your API keys:

#### Create Bing Web Search API Key
To create [Bing Web Search](https://www.microsoft.com/en-us/bing/apis/pricing){target="_blank"} API key, follow the guide provided.

!!! note
    You will need to create **Microsoft Azure** Account.


{! docs/en/snippets/creating_whatsapp_api_key.md !}

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

### Workflow Code
{! docs/en/tutorials/mesop_template.md[ln:108-112] !}

<details>
<summary>workflow.py</summary>
```python
{! docs_src/tutorials/whatsapp/main.py !}
```
</details>

### Deployment Code
{! docs/en/tutorials/mesop_template.md[ln:116-127] !}


## Code Walkthrough

Now we will go over each key part of the code, explaining its function and purpose within the FastAgency framework. Understanding these components is crucial for building a dynamic interaction between the user, the [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md), and the **WhatsAppAgent**.

### Creating the WhatsApp API Instance
The following lines shows how to initializes the WhatsApp API by loading the OpenAPI specification from a URL. The OpenAPI spec defines how to interact with the WhatsApp API, including endpoints, parameters, and security details.

Also, we configure the **WhatsApp API** with the __*WHATSAPP_API_KEY*__ using __*set_security_params*__ to authenticate our requests.
```python
{! docs_src/tutorials/whatsapp/main.py [ln:24-34] !}
```

For more information, visit [**API Integration User Guide**](../../user-guide/api/index.md){target="_blank"}.


### Registering the Workflow

Here, we initialize a new workflow using ***AutoGenWorkflows()*** and register it under the name ***"whatsapp_and_websurfer"***. The ***@wf.register*** decorator registers the function to handle chat flow with security enabled, combining both WhatsAppAgent and WebSurferAgent.

```python
{! docs_src/tutorials/whatsapp/main.py [ln:63-64] !}
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
{! docs_src/tutorials/whatsapp/main.py [ln:80-97] !}
```


### Registering Functions

The function ***present_completed_task_or_ask_question*** is registered to allow the **WhatsAppAgent** to ask questions or present completed tasks after receiving data from the [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md).

```python
{! docs_src/tutorials/whatsapp/main.py [ln:98-106] !}
```


We register the WhatsApp API, which allows the **WhatsAppAgent** to handle tasks like suggesting messages that will be sent to the user.
```python
{! docs_src/tutorials/whatsapp/main.py [ln:107-113] !}
```

### Initiating the Chat

We initiate the conversation between the user, [**`WebSurferAgent`**](../../api/fastagency/runtimes/autogen/agents/websurfer/WebSurferAgent.md), and **WhatsAppAgent**. The user’s initial message is provided, and the system is configured to handle up to 10 turns of interaction. The conversation is summarized using the ***reflection_with_llm*** method, which uses a language model to summarize the chat.

Once the conversation ends, the summary is returned to the user, wrapping up the session.

```python
{! docs_src/tutorials/whatsapp/main.py [ln:120-127] !}
```

### Starting the Application

{! docs/en/tutorials/mesop_template.md[ln:132-138] !}

## Running the Application

{! docs/en/tutorials/mesop_template.md[ln:143-178] !}


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
