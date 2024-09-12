# OpenAPI

FastAgency can automatically create functions properly annotated for use with LLM-s from [OpenAPI](https://swagger.io/specification/) specification.

This example demonstrates how to integrate external REST API calls into `AutoGen` agents using `FastAgency`. We'll create a weather agent that interacts with a weather REST API and a user agent to facilitate the conversation. This example will help you understand how to set up agents and facilitate agent communication through an external REST API. To interact with the REST API, the AutoGen agent needs to understand the available routes, so it requires the OpenAPI specification (`openapi.json` file) for the external REST API.

In this example, we'll use a simple [weather API](https://weather.tools.fastagency.ai/docs){target="_blank"} and its specification available at [https://weather.tools.fastagency.ai/openapi.json](https://weather.tools.fastagency.ai/openapi.json){target="_blank"}.

!!! note
    The [weather API](https://weather.tools.fastagency.ai/docs){target="_blank"} has two routes: one for the daily weather forecast, which has no security, and another for the hourly forecast, which is secured. We will learn how to access external APIs that are secured in the [next chapter](../security.md){.internal-link}.

## Install

To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```console
pip install "fastagency[autogen,openapi]"
```

## Imports
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the `OpenAPI` Client and `UserProxyAgent`:

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:1-10] !}
```

## Define Workflow

In this workflow, the only difference is that we create a Python client for the external REST API by passing the URL of the `openapi.json` to the `Client.create` method. Then, we register the generated client with the agent using the methods `register_for_llm` and `register_for_execution`. Here's a simple example of a workflow definition:

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:12-55] !}
```

This code snippet sets up a simple weather agent that calls an external weather API using the registered functions generated from the `openapi.json` URL.

## Define FastAgency Application

Next, define your FastAgency application.

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:58] !}
```

## Run Application

You can run this chapter's FastAgency application using the following command:

```console
fastagency run docs/docs_src/user_guide/external_rest_apis/main.py
```

## Output

The output will vary based on the city and the current weather conditions:

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
 │              └── 🐍 main.py         │
 │                                     │
 ╰─────────────────────────────────────╯

 ╭─────────────────── Importable FastAgency app ────────────────────╮
 │                                                                  │
 │  from docs.docs_src.tutorial.external_rest_apis.main import app  │
 │                                                                  │
 ╰──────────────────────────────────────────────────────────────────╯

╭─ FastAgency -> user [text_input] ────────────────────────────────────────────╮
│                                                                              │
│ Starting a new workflow 'simple_weather' with the following                  │
│ description:                                                                 │
│                                                                              │
│ Weather chat                                                                 │
│                                                                              │
│ Please enter an initial message:                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
Get me daily weather forecast for Chennai city

    ╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ Get me daily weather forecast for Chennai city                               │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [suggested_function_call] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_daily_weather_daily_get",                            │
    │   "call_id":                                                                 │
    │ "call_VZ19VFNcTE9n8BnXa9aiMzFA",                                             │
    │   "arguments": {                                                             │
    │     "city":                                                                  │
    │ "Chennai"                                                                    │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ User_Agent -> Weather_Agent [function_call_execution] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_daily_weather_daily_get",                            │
    │   "call_id":                                                                 │
    │ "call_VZ19VFNcTE9n8BnXa9aiMzFA",                                             │
    │   "retval": "{\"city\": \"Chennai\",                                         │
    │ \"temperature\": 31, \"daily_forecasts\": [{\"forecast_date\":               │
    │ \"2024-09-10\", \"temperature\": 31, \"hourly_forecasts\": null},            │
    │ {\"forecast_date\": \"2024-09-11\", \"temperature\": 30,                     │
    │ \"hourly_forecasts\": null}, {\"forecast_date\": \"2024-09-12\",             │
    │ \"temperature\": 30, \"hourly_forecasts\": null}]}\n"                        │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ The daily weather forecast for Chennai is as follows:                        │
    │                                                                              │
    │ - **September                                                                │
    │ 10, 2024**: Temperature - 31°C                                               │
    │ - **September 11, 2024**: Temperature -                                      │
    │  30°C                                                                        │
    │ - **September 12, 2024**: Temperature - 30°C                                 │
    │                                                                              │
    │ If you need more                                                             │
    │ details or forecasts for more days, feel free to ask!                        │
    ╰──────────────────────────────────────────────────────────────────────────────╯
```
