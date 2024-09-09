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
{! docs_src/tutorial/external_rest_apis/main.py [ln:12-54] !}
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
