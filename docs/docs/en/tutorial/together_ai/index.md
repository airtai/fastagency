# Using Non-OpenAI Models with FastAgency

In this tutorial, you'll learn how to use **non-OpenAI models with FastAgency**. Since FastAgency uses AutoGen as its default runtime, it automatically supports all proxy servers that are AutoGen compatible. For more information on the supported proxy servers, please see <a href="https://microsoft.github.io/autogen/0.2/docs/topics/non-openai-models/about-using-nonopenai-models" target="_blank" >here</a>.

To keep things simple and demonstrate the use of non-OpenAI models, we’ll recreate the **Weatherman** example mentioned in this [section](../../user-guide/api/openapi/index.md) using  **Together AI Cloud along with the powerful Meta-Llama-3.1-70B-Instruct-Turbo** model. Let’s get started!

## What You’ll Learn

By the end of this tutorial, you’ll learn how to:

- **Utilize non-OpenAI** models with FastAgency.
- Set up and configure **Together AI Cloud and the Meta-Llama-3.1-70B-Instruct-Turbo** model for your applications.
- Build and register agents that can effectively use non-OpenAI models.
- Use FastAgency workflows to manage agent interactions and user input.

Let’s get started with using non-OpenAI models in **FastAgency!**

## Prerequisites

Before you begin this tutorial, ensure you have the following:

- **FastAgency installed**: Follow the installation instructions mentioned [here](#installing-fastagency) for installing FastAgency.
- **Together AI account and API Key**: For details on how to create an account and obtain your API key, see the [Setting Up Your Together AI Account and API Key section](#setting-up-your-together-ai-account-and-api-key).

With these prerequisites in place, you’re ready to dive into the tutorial!

## Installation and Together AI API Key Setup

In this section, we'll go through the steps to install FastAgency and set up your Together AI API key.

### Installing FastAgency

To get started, you need to install FastAgency with autogen submodule. You can do this using `pip`, Python's package installer.

```bash
pip install "fastagency[autogen,openapi]"
```

### Setting Up Your Together AI Account and API Key

1. Create a Together AI account:

    - Go to <a href="https://api.together.ai" target="_blank">https://api.together.ai</a>.
    - Click on one of the options to Sign in and follow the instructions to create your account.
    - If you already have an account, simply log in.

2. Obtain your API Key:

    - Once you complete the account creation process the API key will be displayed on the screen which you can copy.
    - Or you can do the following to view your API key:
        - Tap on the person icon at the top right corner, and click **Settings**
        - On the left side bar, navigate to **API Keys**
        - **Copy your API key**, and you're ready to go!

#### Set Up Your API Keys in the Environment

To securely use the API keys in your project, you should store it in an environment variables.

You can set the API keys in your terminal as an environment variable:

=== "Linux/macOS"
    ```bash
    export TOGETHER_API_KEY="your_together_api_key"  # pragma: allowlist secret
    ```
=== "Windows"
    ```bash
    set TOGETHER_API_KEY="your_together_api_key"  # pragma: allowlist secret
    ```

## Code Walkthrough

Since we are recreating an [existing example](../../user-guide/api/openapi/index.md) with non-OpenAI models, most of the code remains the same, with just a few changes:

- **Configure the Language Model (LLM)**
- **Update the System Message**

These are the only modifications made to the original code, demonstrating how easy it is to switch to a non-OpenAI model with just a few lines of code.

### Configure the Language Model (LLM)

In this step, the large language model is configured to use the `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo` model. The `API` key is retrieved from the `TOGETHER_API_KEY` environment variable, and the `api_type` is set to `together`.

```python
{! docs_src/tutorial/together_ai/main.py [ln:12-22] !}
```

### Update the System Message

The system message has been updated to work with the `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo` model

```python
{! docs_src/tutorial/together_ai/main.py [ln:27] !}
```

## Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/tutorial/together_ai/main.py !}
```
</details>

## Running the Application

Once the workflow is set up, you can run the application using the **FastAgency CLI**. Navigate to the directory where the script is located and run the following command:

```bash
fastagency run
```

## Output

The output will vary based on the city and the current weather conditions:

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

╭─ FastAgency -> user [workflow_started] ──────────────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "name": "simple_weather",                                                  │
│   "description": "Weather chat",                                             │
│                                                                              │
│ "params": {}                                                                 │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ I can help you with the weather. What would you like to know?:               │
    ╰──────────────────────────────────────────────────────────────────────────────╯
What's the weather in Zagreb
╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
│                                                                              │
│ What's the weather in Zagreb                                                 │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
│                                                                              │
│ Please wait while I fetch the weather data for Zagreb...                     │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ User_Agent -> Weather_Agent [suggested_function_call] ──────────────────────╮
│                                                                              │
│ {                                                                            │
│   "function_name": "get_daily_weather_daily_get",                            │
│   "call_id":                                                                 │
│ "call_fwdnhh2bptuauqqniiwha4g7",                                             │
│   "arguments": {                                                             │
│     "city": "Zagreb"                                                         │
│                                                                              │
│   }                                                                          │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Weather_Agent -> User_Agent [function_call_execution] ──────────────────────╮
│                                                                              │
│ {                                                                            │
│   "function_name": "get_daily_weather_daily_get",                            │
│   "call_id":                                                                 │
│ "call_fwdnhh2bptuauqqniiwha4g7",                                             │
│   "retval": "{\"city\": \"Zagreb\",                                          │
│ \"temperature\": 17, \"daily_forecasts\": [{\"forecast_date\":               │
│ \"2024-10-14\", \"temperature\": 14, \"hourly_forecasts\": null},            │
│ {\"forecast_date\": \"2024-10-15\", \"temperature\": 15,                     │
│ \"hourly_forecasts\": null}, {\"forecast_date\": \"2024-10-16\",             │
│ \"temperature\": 15, \"hourly_forecasts\": null}]}\n"                        │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
│                                                                              │
│ The current weather in Zagreb is 17 degrees Celsius. The forecast for        │
│ the next few days is as follows:                                             │
│                                                                              │
│ - October 14, 2024: 14 degrees                                               │
│ Celsius                                                                      │
│ - October 15, 2024: 15 degrees Celsius                                       │
│ - October 16, 2024: 15                                                       │
│ degrees Celsius                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
│                                                                              │
│ The current weather in Zagreb is 17 degrees Celsius. The forecast for        │
│ the next few days is as follows:                                             │
│                                                                              │
│ - October 14, 2024: 14 degrees                                               │
│ Celsius                                                                      │
│ - October 15, 2024: 15 degrees Celsius                                       │
│ - October 16, 2024: 15                                                       │
│ degrees Celsius                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ AutoGenWorkflows -> user [workflow_completed] ──────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "result": {                                                                │
│     "content": "The current weather in Zagreb is 17                          │
│ degrees Celsius, with forecasted temperatures of 14 degrees Celsius on       │
│  October 14, 15 degrees Celsius on October 15, and 15 degrees Celsius        │
│ on October 16.",                                                             │
│     "refusal": null,                                                         │
│     "role": "assistant",                                                     │
│                                                                              │
│ "function_call": null,                                                       │
│     "tool_calls": null                                                       │
│   }                                                                          │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

2024-10-14 19:37:11,923 [INFO] Workflow 'simple_weather' completed with result: {'content': 'The current weather in Zagreb is 17 degrees Celsius, with forecasted temperatures of 14 degrees Celsius on October 14, 15 degrees Celsius on October 15, and 15 degrees Celsius on October 16.', 'refusal': None, 'role': 'assistant', 'function_call': None, 'tool_calls': None}
```

## Conclusion

In this tutorial, we explored how to **leverage non-OpenAI models with FastAgency** by making just a few lines of code changes to an existing example. By configuring the Language Model (LLM) and updating the system message, we demonstrated how simple it is to switch to a different model, specifically the `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo`.

You’ve learned how to:

- **Configure a non-OpenAI model** within FastAgency.
- Update system messages to optimize interactions with different models.
- **Easily transition between models** with minimal code changes.

With these skills, you now have the foundation to integrate other non-OpenAI models into your projects, opening up new possibilities for building robust and diverse applications.
