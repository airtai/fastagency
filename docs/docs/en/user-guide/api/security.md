# Security

In the [previous chapter](./index.md){.internal-link}, we learned how to integrate external REST APIs into `AutoGen` agents using `FastAgency`, and we used a weather API route which had no security. However, not all external REST APIs are open to the public; some are behind a paywall and require security parameters for access. This section of the documentation explains how to create an agent that accesses an external REST API with security.

For this tutorial, the [weather API](https://weather.tools.fastagency.ai/docs) provides an hourly forecast route that is secured.

!!! note
    The [weather API](https://weather.tools.fastagency.ai/docs){target="_blank"} offers two routes: one for the daily weather forecast, which has no security, and another for the hourly forecast, which is secured. To learn how to access external APIs that are not secured, please refer to the [previous chapter](./index.md){.internal-link}.

## Install

The installation process is exactly the same as in the [previous chapter](./index.md){.internal-link}.

```console
pip install "fastagency[autogen,openapi]"
```

## Imports
The imports are the same as in the [previous chapter](./index.md){.internal-link}, except here we also import `APIKeyHeader` to set the security value in the header:

```python hl_lines="8"
{! docs_src/user_guide/external_rest_apis/security.py [ln:1-10] !}
```

## Configure the Language Model (LLM)
Here, the large language model is configured to use the `gpt-4o-mini` model, and the API key is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:11-20] !}
```

## Set Up the Weather API
We define the OpenAPI specification URL for the weather service. This API will later be used by the weather agent to fetch real-time weather data.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:22,23] !}
```

## Configuring API Security Parameters

Here, we define security settings for the weather API by setting API keys for authentication. This ensures secure access when interacting with the API, globally across all methods.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:25,26] !}
```

You can also set security parameters for a specific method. The code below demonstrates how to apply security parameters to a specific method instead of globally. In this example, the security settings are only applied to the `get_daily_weather_daily_get` method.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:28-32] !}
```

## Define the Workflow and Agents

In this step, we define two agents and specify the initial message that will be displayed to users when the workflow starts.

- **UserProxyAgent**: This agent simulates the user interacting with the system.

- **ConversableAgent**: This agent acts as the weather agent, responsible for fetching weather data from the API.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:34-61] !}
```

## Register API Functions with the Agents
In this step, we register the weather API functions to ensure that the weather agent can call the correct functions to retrieve the required weather data.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:62-67] !}
```

## Enable Agent Interaction and Chat
Here, the user agent initiates a chat with the weather agent, which queries the API and returns the weather information. The conversation is summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:68-76] !}
```

## Define FastAgency Application

Next, define your FastAgency application.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:79] !}
```

## Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/external_rest_apis/security.py !}
```
</details>


## Run Application

You can run this chapter's FastAgency application using the following command::

```console
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
│   "name": "simple_weather_with_security",                                    │
│   "description": "Weather                                                    │
│ chat with security",                                                         │
│   "params": {}                                                               │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Workflow -> User [text_input] ──────────────────────────────────────────────╮
    │                                                                              │
    │ What do you want to know about the weather?:                                 │
    ╰──────────────────────────────────────────────────────────────────────────────╯

Get me daily weather forecast for Chennai city
    ╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ Get me daily weather forecast for Chennai city                               │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ I'm unable to provide real-time weather forecasts. However, you can          │
    │ easily find the daily weather forecast for Chennai by checking               │
    │ reliable weather websites, using weather apps, or searching for              │
    │ "Chennai weather forecast" in your preferred search engine. If you           │
    │ have any other questions or need information about typical weather           │
    │ patterns in Chennai, feel free to ask!                                       │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ User_Agent -> Weather_Agent [suggested_function_call] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_daily_weather_daily_get",                            │
    │   "call_id":                                                                 │
    │ "call_lbik8BJJREriUyhbpuKE5hhC",                                             │
    │   "arguments": {                                                             │
    │     "city":                                                                  │
    │ "Chennai"                                                                    │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [function_call_execution] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_daily_weather_daily_get",                            │
    │   "call_id":                                                                 │
    │ "call_lbik8BJJREriUyhbpuKE5hhC",                                             │
    │   "retval": "{\"city\": \"Chennai\",                                         │
    │ \"temperature\": 30, \"daily_forecasts\": [{\"forecast_date\":               │
    │ \"2024-10-10\", \"temperature\": 29, \"hourly_forecasts\": null},            │
    │ {\"forecast_date\": \"2024-10-11\", \"temperature\": 29,                     │
    │ \"hourly_forecasts\": null}, {\"forecast_date\": \"2024-10-12\",             │
    │ \"temperature\": 28, \"hourly_forecasts\": null}]}\n"                        │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ Here is the daily weather forecast for Chennai:                              │
    │                                                                              │
    │ - **October 10,                                                              │
    │ 2024**: Temperature - 29°C                                                   │
    │ - **October 11, 2024**: Temperature - 29°C                                   │
    │                                                                              │
    │ - **October 12, 2024**: Temperature - 28°C                                   │
    │                                                                              │
    │ If you need more details                                                     │
    │ or hourly forecasts, let me know!                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ Here is the daily weather forecast for Chennai:                              │
    │                                                                              │
    │ - **October 10,                                                              │
    │ 2024**: Temperature - 29°C                                                   │
    │ - **October 11, 2024**: Temperature - 29°C                                   │
    │                                                                              │
    │ - **October 12, 2024**: Temperature - 28°C                                   │
    │                                                                              │
    │ If you need more details                                                     │
    │ or hourly forecasts, feel free to ask!                                       │
    ╰──────────────────────────────────────────────────────────────────────────────╯

╭─ workflow -> user [workflow_completed] ──────────────────────────────────────╮
│                                                                              │
│ {                                                                            │
│   "result": "The user requested the daily weather forecast for               │
│ Chennai, and the assistant provided the forecast for October 10, 11,         │
│ and 12, 2024, with temperatures of 29\u00b0C, 29\u00b0C, and                 │
│ 28\u00b0C, respectively. The assistant also offered to provide more          │
│ details or hourly forecasts if needed."                                      │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```
