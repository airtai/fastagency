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
