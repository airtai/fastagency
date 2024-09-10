# Using External REST APIs

FastAgency can automatically create functions properly annotated for use with LLM-s from [OpenAPI](https://swagger.io/specification/) specification.

This example demonstrates how to integrate external REST API calls into `AutoGen` agents using `FastAgency`. We'll create a weather agent that interacts with a weather REST API and a user agent to facilitate the conversation. This example will help you understand how to set up agents and facilitate agent communication through an external REST API. To interact with the REST API, the AutoGen agent needs to understand the available routes, so it requires the OpenAPI specification (`openapi.json` file) for the external REST API.

In this example, we'll use a simple [weather API](https://weather.tools.fastagency.ai/docs){target="_blank"} and its specification available at [https://weather.tools.fastagency.ai/openapi.json](https://weather.tools.fastagency.ai/openapi.json){target="_blank"}.

## Install

To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```console
pip install "fastagency[autogen,openapi]"
```

## Imports
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the `OpenAPI` Client and `UserProxyAgent`:

```python
{! docs_src/tutorial/external_rest_apis/main.py [ln:1-10] !}
```

## Define Workflow

In this workflow, the only difference is that we create a Python client for the external REST API by passing the URL of the `openapi.json` to the `Client.create` method. Then, we register the generated client with the agent using the methods `register_for_llm` and `register_for_execution`. Here's a simple example of a workflow definition:

```python
{! docs_src/tutorial/external_rest_apis/main.py [ln:12-55] !}
```

This code snippet sets up a simple weather agent that calls an external weather API using the registered functions generated from the `openapi.json` URL.

## Define FastAgency Application

Next, define your FastAgency application.

```python
{! docs_src/tutorial/external_rest_apis/main.py [ln:58] !}
```

## Run Application

Once everything is set up, you can run your FastAgency application using the following command:

```console
fastagency run
```

## Output

The output will vary based on the city and the current weather conditions:

```console

 ╭── Python module file ──╮
 │                        │
 │  🐍 sample_weather.py  │
 │                        │
 ╰────────────────────────╯

 ╭─── Importable FastAgency app ────╮
 │                                  │
 │  from sample_weather import app  │
 │                                  │
 ╰──────────────────────────────────╯

╭─ FastAgency -> user [text_input] ────────────────────────────────────────────╮
│                                                                              │
│ Starting a new workflow 'simple_weather' with the following                  │
│ description:                                                                 │
│                                                                              │
│ Weather chat                                                                 │
│                                                                              │
│ Please enter an initial message:                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
What is the weather in Zagreb?
    ╭─ User_Agent -> Weather_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ What is the weather in Zagreb?                                               │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [suggested_function_call] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_weather__get",                                       │
    │   "call_id":                                                                 │
    │ "call_gGl4uAhMvPTXjgrOvkVZwCh3",                                             │
    │   "arguments": {                                                             │
    │     "city": "Zagreb"                                                         │
    │                                                                              │
    │   }                                                                          │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ User_Agent -> Weather_Agent [function_call_execution] ──────────────────────╮
    │                                                                              │
    │ {                                                                            │
    │   "function_name": "get_weather__get",                                       │
    │   "call_id":                                                                 │
    │ "call_gGl4uAhMvPTXjgrOvkVZwCh3",                                             │
    │   "retval": "{\"city\": \"Zagreb\",                                          │
    │ \"temperature\": 18, \"daily_forecasts\": [{\"forecast_date\":               │
    │ \"2024-09-06\", \"temperature\": 23, \"hourly_forecasts\":                   │
    │ [{\"forecast_time\": \"00:00:00\", \"temperature\": 19,                      │
    │ \"description\": \"Patchy rain nearby\"}, {\"forecast_time\":                │
    │ \"03:00:00\", \"temperature\": 19, \"description\": \"Patchy light           │
    │ drizzle\"}, {\"forecast_time\": \"06:00:00\", \"temperature\": 18,           │
    │ \"description\": \"Clear\"}, {\"forecast_time\": \"09:00:00\",               │
    │ \"temperature\": 24, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"12:00:00\", \"temperature\": 30, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"15:00:00\", \"temperature\": 30,                       │
    │ \"description\": \"Partly Cloudy\"}, {\"forecast_time\": \"18:00:00\",       │
    │  \"temperature\": 26, \"description\": \"Patchy rain nearby\"},              │
    │ {\"forecast_time\": \"21:00:00\", \"temperature\": 21,                       │
    │ \"description\": \"Patchy rain nearby\"}]}, {\"forecast_date\":              │
    │ \"2024-09-07\", \"temperature\": 24, \"hourly_forecasts\":                   │
    │ [{\"forecast_time\": \"00:00:00\", \"temperature\": 19,                      │
    │ \"description\": \"Partly Cloudy\"}, {\"forecast_time\": \"03:00:00\",       │
    │  \"temperature\": 18, \"description\": \"Clear\"}, {\"forecast_time\":       │
    │  \"06:00:00\", \"temperature\": 18, \"description\": \"Clear\"},             │
    │ {\"forecast_time\": \"09:00:00\", \"temperature\": 25,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"12:00:00\",               │
    │ \"temperature\": 30, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"15:00:00\", \"temperature\": 31, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"18:00:00\", \"temperature\": 26,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"21:00:00\",               │
    │ \"temperature\": 22, \"description\": \"Clear\"}]},                          │
    │ {\"forecast_date\": \"2024-09-08\", \"temperature\": 25,                     │
    │ \"hourly_forecasts\": [{\"forecast_time\": \"00:00:00\",                     │
    │ \"temperature\": 20, \"description\": \"Partly Cloudy\"},                    │
    │ {\"forecast_time\": \"03:00:00\", \"temperature\": 19,                       │
    │ \"description\": \"Clear\"}, {\"forecast_time\": \"06:00:00\",               │
    │ \"temperature\": 18, \"description\": \"Clear\"}, {\"forecast_time\":        │
    │ \"09:00:00\", \"temperature\": 26, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"12:00:00\", \"temperature\": 31,                       │
    │ \"description\": \"Sunny\"}, {\"forecast_time\": \"15:00:00\",               │
    │ \"temperature\": 32, \"description\": \"Sunny\"}, {\"forecast_time\":        │
    │ \"18:00:00\", \"temperature\": 27, \"description\": \"Sunny\"},              │
    │ {\"forecast_time\": \"21:00:00\", \"temperature\": 23,                       │
    │ \"description\": \"Partly Cloudy\"}]}]}\n"                                   │
    │ }                                                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    ╭─ Weather_Agent -> User_Agent [text_message] ─────────────────────────────────╮
    │                                                                              │
    │ The current weather in Zagreb is 18°C. Here are the upcoming weather         │
    │ forecasts:                                                                   │
    │                                                                              │
    │ ### September 6, 2024                                                        │
    │ - **Day Temperature**: 23°C                                                  │
    │ -                                                                            │
    │ **Hourly Forecast**:                                                         │
    │   - 00:00: 19°C - Patchy rain nearby                                         │
    │   - 03:00:                                                                   │
    │ 19°C - Patchy light drizzle                                                  │
    │   - 06:00: 18°C - Clear                                                      │
    │   - 09:00: 24°C -                                                            │
    │ Sunny                                                                        │
    │   - 12:00: 30°C - Sunny                                                      │
    │   - 15:00: 30°C - Partly Cloudy                                              │
    │   -                                                                          │
    │ 18:00: 26°C - Patchy rain nearby                                             │
    │   - 21:00: 21°C - Patchy rain nearby                                         │
    │                                                                              │
    │                                                                              │
    │ ### September 7, 2024                                                        │
    │ - **Day Temperature**: 24°C                                                  │
    │ - **Hourly                                                                   │
    │ Forecast**:                                                                  │
    │   - 00:00: 19°C - Partly Cloudy                                              │
    │   - 03:00: 18°C - Clear                                                      │
    │                                                                              │
    │ - 06:00: 18°C - Clear                                                        │
    │   - 09:00: 25°C - Sunny                                                      │
    │   - 12:00: 30°C - Sunny                                                      │
    │                                                                              │
    │   - 15:00: 31°C - Sunny                                                      │
    │   - 18:00: 26°C - Sunny                                                      │
    │   - 21:00: 22°C -                                                            │
    │ Clear                                                                        │
    │                                                                              │
    │ ### September 8, 2024                                                        │
    │ - **Day Temperature**: 25°C                                                  │
    │ - **Hourly                                                                   │
    │ Forecast**:                                                                  │
    │   - 00:00: 20°C - Partly Cloudy                                              │
    │   - 03:00: 19°C - Clear                                                      │
    │                                                                              │
    │ - 06:00: 18°C - Clear                                                        │
    │   - 09:00: 26°C - Sunny                                                      │
    │   - 12:00: 31°C - Sunny                                                      │
    │                                                                              │
    │   - 15:00: 32°C - Sunny                                                      │
    │   - 18:00: 27°C - Sunny                                                      │
    │   - 21:00: 23°C -                                                            │
    │ Partly Cloudy                                                                │
    │                                                                              │
    │ If you need more information, feel free to ask!                              │
    ╰──────────────────────────────────────────────────────────────────────────────╯
```

## Accessing External REST API with security

In previous section, we learned how to integrate external REST APIs into `AutoGen` agents using `FastAgency` and it used a weather API which has no security in it. Not all the external REST APIs are open to public, some are behind a paywall and needs securiyt parameters to access them. This section of documentation helps with creating an agent which accesses an external REST API with security.

Let us build a gif search engine using giphy's APIs. Giphy does not provides an openapi.json so we provide one [here](https://raw.githubusercontent.com/airtai/fastagency/main/examples/openapi/giphy_openapi.json).
