# Using Non-OpenAI Models with FastAgency

FastAgency makes it simple to use **non-OpenAI models** through AutoGen's runtime, which connects to proxy servers offering OpenAI-compatible API. This allows you to create agents using a wide variety of models. For more details on supported proxy servers, check <a href="https://microsoft.github.io/autogen/0.2/docs/topics/non-openai-models/about-using-nonopenai-models" target="_blank" >here</a>.

With this flexibility, you can **access a broad range of models**, **assign specialized models to agents**, **run workflows locally**, and **optimise inference costs** for better efficiency.

To show how simple it is to use **non-OpenAI models**, we’ll **rewrite** the [Weatherman chatbot](./index.md#example-integrating-a-weather-api-with-autogen) example from earlier, making just a **few changes** to switch to **Together AI** Cloud with the **Meta-Llama-3.1-70B-Instruct-Turbo** model. Let’s dive in!

## Installation

Before getting started, make sure you have installed FastAgency with **autogen and openapi submodules** by running the following command:

```bash
pip install "fastagency[autogen,openapi]"
```

This installation includes the AutoGen runtime, allowing you to build multi-agent workflows and integrate external APIs seamlessly.

## Prerequisites

Before you begin this guide, ensure you have:

- **Together AI account and API Key**: For instructions on creating a Together AI account and getting your API key, follow the steps outlined [here](#setting-up-your-together-ai-account-and-api-key) section.

### Setting Up Your Together AI Account and API Key

**1. Create a Together AI account:**

- Go to <a href="https://api.together.ai" target="_blank">https://api.together.ai</a>.
- Click on one of the options to Sign in and follow the instructions to create your account.
- If you already have an account, simply log in.

**2. Obtain your API Key:**

- Once you complete the account creation process the API key will be displayed on the screen which you can copy.
- Or you can do the following to view your API key:
    - Tap on the person icon at the top right corner, and click **Settings**
    - On the left side bar, navigate to **API Keys**
    - **Copy your API key**, and you're ready to go!

#### Set Up Your API Keys in the Environment

To securely use the API keys in your project, you should store it in an environment variables.

You can set the together API key in your terminal as an environment variable:

=== "Linux/macOS"
    ```bash
    export TOGETHER_API_KEY="your_together_api_key"  # pragma: allowlist secret
    ```
=== "Windows"
    ```bash
    set TOGETHER_API_KEY="your_together_api_key"  # pragma: allowlist secret
    ```

## Example: Integrating a Weather API with AutoGen

### Code Walkthrough

As we rewrite the existing [Weatherman chatbox](./index.md#example-integrating-a-weather-api-with-autogen) to use **non-OpenAI models**, most of the code remains unchanged. The only modifications to the original code are:

- **Configure the Language Model (LLM)**
- **Update the System Message**

Since the modifications are minor, **I will focus only on these differences in this guide**. For a **detailed explanation** of the original code, please refer to the original [guide](./index.md#example-integrating-a-weather-api-with-autogen).

#### 1. Configure the Language Model (LLM)

The first and most important change is to update the LLM configuration **to use non-OpenAI models**. In this example, we’ll use **meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo**, but you can choose any models offered by Together AI Cloud. Additionally, we need to add two more parameters: **api_type** and **hide_tools**.

The **hide_tools** parameter is particularly useful, as it prevents tools from appearing in the Together AI response creation call if they have already been executed. This helps minimize the chances of the LLM choosing a tool when it's unnecessary.

Here we are setting `hide_tools` to `if_any_run`, indicating that we want to hide the tools if any of the tools have already been run.

```python
{! docs_src/user_guide/runtimes/autogen/using_non_openai_models.py [ln:12-22] !}
```

#### 2. Update the System Message

The system message has been adjusted to work optimally with the **meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo** model. You may need to experiment with the system prompt if you are using a different model.

```python
{! docs_src/user_guide/runtimes/autogen/using_non_openai_models.py [ln:27] !}
```

### Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/runtimes/autogen/using_non_openai_models.py !}
```
</details>

### Running the Application

Once the workflow is set up, you can run the application using the **FastAgency CLI**. Navigate to the directory where the script is located and run the following command:

```bash
fastagency run
```

### Output

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

This example demonstrates the power of the AutoGen runtime within FastAgency, showcasing how to **leverage non-OpenAI models with FastAgency** by making just a few lines of code. By leveraging FastAgency, developers can quickly build interactive, scalable applications that interact with live data sources.
