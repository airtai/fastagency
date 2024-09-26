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

```console
pip install "fastagency[autogen,openapi]"
```

### Giphy API Key Setup
The **GiphyAgent** requires an API key to interact with Giphy's service. Follow these steps to create your API key:

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

#### Set Up Your API Key in the Environment

To securely use the API key in your project, you should store it in an environment variable.

You can set the Giphy API key in your terminal as an environment variable:

=== "Linux/macOS"
    ```console
    export GIPHY_API_KEY="your_giphy_api_key"
    ```
=== "Windows"
    ```console
    set GIPHY_API_KEY="your_giphy_api_key"
    ```
