# OpenAPI

FastAgency can automatically create functions properly annotated for use with LLM-s from [OpenAPI](https://swagger.io/specification/) specification.

This example demonstrates how to integrate external REST API calls into `AG2` agents using `FastAgency`. We'll create a weather agent that interacts with a weather REST API and a user agent to facilitate the conversation. This example will help you understand how to set up agents and facilitate agent communication through an external REST API. To interact with the REST API, the AG2 agent needs to understand the available routes, so it requires the OpenAPI specification (`openapi.json` file) for the external REST API.

In this example, we'll use a simple [weather API](https://weather.tools.fastagency.ai/docs){target="_blank"} and its specification available at [https://weather.tools.fastagency.ai/openapi.json](https://weather.tools.fastagency.ai/openapi.json){target="_blank"}.

!!! note
    The [weather API](https://weather.tools.fastagency.ai/docs){target="_blank"} has two routes: one for the daily weather forecast, which has no security, and another for the hourly forecast, which is secured. We will learn how to access external APIs that are secured in the [next chapter](../security.md){.internal-link}.

## Install

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**. Before getting started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

```console
pip install "fastagency[autogen,openapi]"
```

## Imports
These imports are similar to the imports section we have already covered, with the only difference being the additional imports of the `OpenAPI` Client and `UserProxyAgent`:

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:1-9] !}
```

## Configure the Language Model (LLM)
Here, the large language model is configured to use the `gpt-4o-mini` model, and the API key is retrieved from the environment. This setup ensures that both the user and weather agents can interact effectively.

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:11-19] !}
```

## Set Up the Weather API
We define the OpenAPI specification URL for the weather service. This API will later be used by the weather agent to fetch real-time weather data.

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:21-22] !}
```

## Define the Workflow and Agents

In this step, we define two agents and specify the initial message that will be displayed to users when the workflow starts.

- **UserProxyAgent**: This agent simulates the user interacting with the system.

- **ConversableAgent**: This agent acts as the weather agent, responsible for fetching weather data from the API.

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:24-48] !}
```

## Register API Functions with the Agents
In this step, we register the weather API functions to ensure that the weather agent can call the correct functions to retrieve the required weather data.

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:50-54] !}
```

## Enable Agent Interaction and Chat
Here, the user agent initiates a chat with the weather agent, which queries the API and returns the weather information. The conversation is summarized using a method provided by the LLM.

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:56-63] !}
```

## Define FastAgency Application

Next, define your FastAgency application.

```python
{! docs_src/user_guide/external_rest_apis/main.py [ln:66] !}
```

## Complete Application Code

<details>
<summary>main.py</summary>
```python
{! docs_src/user_guide/external_rest_apis/main.py !}
```
</details>


## Run Application

You can run this chapter's FastAgency application using the following command:

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
│   "name": "simple_weather",                                                  │
│   "description": "Weather chat",                                             │
│                                                                              │
│ "params": {}                                                                 │
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
