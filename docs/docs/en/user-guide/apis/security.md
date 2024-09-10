# Using External REST APIs with security

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

```python hl_lines="11"
{! docs_src/user_guide/external_rest_apis/security.py [ln:1-11] !}
```

## Define Workflow

In this workflow, we create a Python client for the external REST API by passing the URL of the `openapi.json` to the `Client.create` method. Then, we register the generated client with the agent using the methods `register_for_llm` and `register_for_execution`.

Additionally, we set the API key for the API using the `set_security_params` method:

```python hl_lines="2"
{! docs_src/user_guide/external_rest_apis/security.py [ln:33.5,34.5] !}
```

Here's a simple example of a workflow definition:

```python hl_lines="22"
{! docs_src/user_guide/external_rest_apis/security.py [ln:13-65] !}
```

This code snippet sets up a simple weather agent that calls an external weather API with security, using the registered functions generated from the `openapi.json` URL.

## Define FastAgency Application

Next, define your FastAgency application.

```python
{! docs_src/user_guide/external_rest_apis/security.py [ln:68] !}
```

## Run Application

You can run this chapter's FastAgency application using the following command::

```console
fastagency run docs/docs_src/user_guide/external_rest_apis/security.py
```

## Output

The output will vary based on the city and current weather conditions:

```console
 ╭─── Python package file structure ───╮
 │                                     │
 │  📁 docs                            │
 │  ├── 🐍 __init__.py                 │
 │  └── 📁 docs_src                    │
 │      ├── 🐍 __init__.py             │
 │      └── 📁 tutorial                │
 │          ├── 🐍 __init__.py         │
 │          └── 📁 external_rest_apis  │
 │              ├── 🐍 __init__.py     │
 │              └── 🐍 security.py     │
 │                                     │
 ╰─────────────────────────────────────╯

 ╭───────────────────── Importable FastAgency app ──────────────────────╮
 │                                                                      │
 │  from docs.docs_src.tutorial.external_rest_apis.security import app  │
 │                                                                      │
 ╰──────────────────────────────────────────────────────────────────────╯

╭─ FastAgency -> user [text_input] ────────────────────────────────────────────╮
│                                                                              │
│ Starting a new workflow 'simple_weather_with_security' with the              │
│ following description:                                                       │
│                                                                              │
│ Weather chat with security                                                   │
│                                                                              │
│ Please enter an                                                              │
│ initial message:                                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
Get me hourly weather forecast for Chennai city
    ╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ Get me hourly weather forecast for Chennai city                              │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [suggested_function_call] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_hourly_weather_hourly_get",                          │
    │   "call_id":                                                                 │
    │ "call_pAMWHJ1wIlsciSSOMIb4uhst",                                             │
    │   "arguments": {                                                             │
    │     "city":                                                                  │
    │ "Chennai"                                                                    │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ User_Agent -> Weather_Agent [function_call_execution] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_hourly_weather_hourly_get",                          │
    │   "call_id":                                                                 │
    │ "call_pAMWHJ1wIlsciSSOMIb4uhst",                                             │
    │   "retval": "{\"city\": \"Chennai\",                                         │
    │ \"temperature\": 35, \"daily_forecasts\": [{\"forecast_date\":               │
    │ \"2024-09-10\", \"temperature\": 31, \"hourly_forecasts\":                   │
    │ [{\"forecast_time\": \"00:00:00\", \"temperature\": 30,                      │
    │ \"description\": \"Patchy rain nearby\"}, {\"forecast_time\":                │
    │ \"03:00:00\", \"temperature\": 29, \"description\": \"Clear\"},              │
    │ {\"forecast_time\": \"06:00:00\", \"temperature\": 28,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"09:00:00\",               │
    │ \"temperature\": 31, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"12:00:00\", \"temperature\": 35, \"description\": \"Partly                 │
    │ cloudy\"}, {\"forecast_time\": \"15:00:00\", \"temperature\": 32,            │
    │ \"description\": \"Patchy light drizzle\"}, {\"forecast_time\":              │
    │ \"18:00:00\", \"temperature\": 30, \"description\": \"Patchy light           │
    │ drizzle\"}, {\"forecast_time\": \"21:00:00\", \"temperature\": 30,           │
    │ \"description\": \"Patchy rain nearby\"}]}, {\"forecast_date\":              │
    │ \"2024-09-11\", \"temperature\": 30, \"hourly_forecasts\":                   │
    │ [{\"forecast_time\": \"00:00:00\", \"temperature\": 29,                      │
    │ \"description\": \"Patchy rain nearby\"}, {\"forecast_time\":                │
    │ \"03:00:00\", \"temperature\": 29, \"description\": \"Clear\"},              │
    │ {\"forecast_time\": \"06:00:00\", \"temperature\": 28,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"09:00:00\",               │
    │ \"temperature\": 31, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"12:00:00\", \"temperature\": 34, \"description\": \"Partly                 │
    │ Cloudy\"}, {\"forecast_time\": \"15:00:00\", \"temperature\": 31,            │
    │ \"description\": \"Cloudy\"}, {\"forecast_time\": \"18:00:00\",              │
    │ \"temperature\": 29, \"description\": \"Partly Cloudy\"},                    │
    │ {\"forecast_time\": \"21:00:00\", \"temperature\": 29,                       │
    │ \"description\": \"Cloudy\"}]}, {\"forecast_date\": \"2024-09-12\",          │
    │ \"temperature\": 30, \"hourly_forecasts\": [{\"forecast_time\":              │
    │ \"00:00:00\", \"temperature\": 29, \"description\": \"Patchy rain            │
    │ nearby\"}, {\"forecast_time\": \"03:00:00\", \"temperature\": 29,            │
    │ \"description\": \"Clear\"}, {\"forecast_time\": \"06:00:00\",               │
    │ \"temperature\": 28, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"09:00:00\", \"temperature\": 31, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"12:00:00\", \"temperature\": 34,                       │
    │ \"description\": \"Partly Cloudy\"}, {\"forecast_time\": \"15:00:00\",       │
    │  \"temperature\": 31, \"description\": \"Partly Cloudy\"},                   │
    │ {\"forecast_time\": \"18:00:00\", \"temperature\": 29,                       │
    │ \"description\": \"Overcast\"}, {\"forecast_time\": \"21:00:00\",            │
    │ \"temperature\": 29, \"description\": \"Partly Cloudy\"}]}]}\n"              │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ Here is the hourly weather forecast for Chennai:                             │
    │                                                                              │
    │ ### September 10,                                                            │
    │ 2024                                                                         │
    │ - **00:00** - Temperature: 30°C, Description: Patchy rain nearby             │
    │                                                                              │
    │ - **03:00** - Temperature: 29°C, Description: Clear                          │
    │ - **06:00** -                                                                │
    │ Temperature: 28°C, Description: Sunny                                        │
    │ - **09:00** - Temperature: 31°C,                                             │
    │  Description: Sunny                                                          │
    │ - **12:00** - Temperature: 35°C, Description:                                │
    │ Partly cloudy                                                                │
    │ - **15:00** - Temperature: 32°C, Description: Patchy                         │
    │ light drizzle                                                                │
    │ - **18:00** - Temperature: 30°C, Description: Patchy                         │
    │ light drizzle                                                                │
    │ - **21:00** - Temperature: 30°C, Description: Patchy                         │
    │ rain nearby                                                                  │
    │                                                                              │
    │ ### September 11, 2024                                                       │
    │ - **00:00** - Temperature: 29°C,                                             │
    │ Description: Patchy rain nearby                                              │
    │ - **03:00** - Temperature: 29°C,                                             │
    │ Description: Clear                                                           │
    │ - **06:00** - Temperature: 28°C, Description: Sunny                          │
    │                                                                              │
    │ - **09:00** - Temperature: 31°C, Description: Sunny                          │
    │ - **12:00** -                                                                │
    │ Temperature: 34°C, Description: Partly Cloudy                                │
    │ - **15:00** -                                                                │
    │ Temperature: 31°C, Description: Cloudy                                       │
    │ - **18:00** - Temperature:                                                   │
    │ 29°C, Description: Partly Cloudy                                             │
    │ - **21:00** - Temperature: 29°C,                                             │
    │ Description: Cloudy                                                          │
    │                                                                              │
    │ ### September 12, 2024                                                       │
    │ - **00:00** - Temperature:                                                   │
    │  29°C, Description: Patchy rain nearby                                       │
    │ - **03:00** - Temperature:                                                   │
    │ 29°C, Description: Clear                                                     │
    │ - **06:00** - Temperature: 28°C, Description:                                │
    │  Sunny                                                                       │
    │ - **09:00** - Temperature: 31°C, Description: Sunny                          │
    │ - **12:00**                                                                  │
    │  - Temperature: 34°C, Description: Partly Cloudy                             │
    │ - **15:00** -                                                                │
    │ Temperature: 31°C, Description: Partly Cloudy                                │
    │ - **18:00** -                                                                │
    │ Temperature: 29°C, Description: Overcast                                     │
    │ - **21:00** - Temperature:                                                   │
    │ 29°C, Description: Partly Cloudy                                             │
    │                                                                              │
    │ Feel free to ask if you need more                                            │
    │ information!                                                                 │
    ╰──────────────────────────────────────────────────────────────────────────────╯
```
