import json
from typing import Any

import pytest
from autogen import ConversableAgent, UserProxyAgent

from fastagency.api.openapi.client import OpenAPI

from ...conftest import create_gify_fastapi_app


@pytest.fixture
def openapi_schema() -> dict[str, Any]:
    app = create_gify_fastapi_app(host="127.0.0.1", port=8000)

    return app.openapi()


def test_openapi_schema(openapi_schema: dict[str, Any]) -> None:
    expected_schema = {
        "openapi": "3.1.0",
        "info": {"title": "Gify", "version": "0.1.0"},
        "servers": [
            {"url": "http://127.0.0.1:8000", "description": "Local development server"}
        ],
        "paths": {
            "/gifs": {
                "get": {
                    "tags": ["gifs"],
                    "summary": "Get Gifs For Topic",
                    "description": "Get GIFs for a topic.",
                    "operationId": "get_gifs_for_topic_gifs_get",
                    "parameters": [
                        {
                            "name": "topic",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string", "title": "Topic"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Gif"},
                                        "title": "Response Get Gifs For Topic Gifs Get",
                                    }
                                }
                            },
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            },
            "/gifs/{gifId}": {
                "get": {
                    "tags": ["gifs"],
                    "summary": "Get Gif By Id",
                    "description": "Get GIF by Id.",
                    "operationId": "get_gif_by_id_gifs__gifId__get",
                    "parameters": [
                        {
                            "name": "gifId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer", "title": "Gifid"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Gif"}
                                }
                            },
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Gif": {
                    "properties": {
                        "id": {"type": "integer", "title": "Id"},
                        "title": {"type": "string", "title": "Title"},
                        "url": {"type": "string", "title": "Url"},
                    },
                    "type": "object",
                    "required": ["id", "title", "url"],
                    "title": "Gif",
                },
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            }
        },
    }

    assert openapi_schema == expected_schema


@pytest.fixture
def api(openapi_schema: dict[str, Any]) -> OpenAPI:
    # print(f"{openapi_schema=}")
    client = OpenAPI.create(json.dumps(openapi_schema))
    return client


def test_register_for_llm(
    api: OpenAPI,
    azure_gpt35_turbo_16k_llm_config: dict[str, Any],
) -> None:
    agent = ConversableAgent(name="agent", llm_config=azure_gpt35_turbo_16k_llm_config)

    api._register_for_llm(agent)
    tools = agent.llm_config["tools"]

    # print(f"{tools=}")

    # the low-level problem
    class JSONEncoder(json.JSONEncoder):
        def default(self, o: Any) -> Any:
            if o.__class__.__name__ == "ellipsis":
                return "Ellipsis"
            return super().default(o)

    expected_tools = [
        {
            "type": "function",
            "function": {
                "description": "Get GIFs for a topic.",
                "name": "get_gifs_for_topic_gifs_get",
                "parameters": {
                    "type": "object",
                    "properties": {"topic": {"type": "string", "description": "topic"}},
                    "required": ["topic"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "description": "Get GIF by Id.",
                "name": "get_gif_by_id_gifs__gif_id__get",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "gif_id": {"type": "integer", "description": "gif_id"}
                    },
                    "required": ["gif_id"],
                },
            },
        },
    ]

    assert json.dumps(tools, cls=JSONEncoder) == json.dumps(
        expected_tools, cls=JSONEncoder
    )


@pytest.mark.azure_oai
def test_end2end(
    gify_fastapi_openapi_url: str,
    azure_gpt35_turbo_16k_llm_config: dict[str, Any],
) -> None:
    api = OpenAPI.create(openapi_url=gify_fastapi_openapi_url)

    agent = ConversableAgent(name="agent", llm_config=azure_gpt35_turbo_16k_llm_config)
    user_proxy = UserProxyAgent(
        name="user_proxy",
        llm_config=azure_gpt35_turbo_16k_llm_config,
        human_input_mode="NEVER",
    )

    api._register_for_llm(agent)
    api._register_for_execution(user_proxy)

    result = user_proxy.initiate_chat(
        agent,
        message="I need the 'url' for gif with id 1",
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    assert "https://gif.example.com/gif1" in result.summary

    result = user_proxy.initiate_chat(
        agent,
        message="I need the all gifs for 'topic' 'funny'. Within the summary, please include the 'url' for each gif.",
        summary_method="reflection_with_llm",
        max_turns=2,
    )

    assert "https://gif.example.com/gif1?topic=funny" in result.summary
    assert "https://gif.example.com/gif2?topic=funny" in result.summary
