import json
from typing import Any

import pytest
from autogen import ConversableAgent, UserProxyAgent

from fastagency.api.openapi.client import OpenAPI


@pytest.fixture
def openapi_schema() -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "My FastAPI app",
            "description": "Test FastAPI app to check OpenAPI schema generation.",
            "version": "0.1.0",
        },
        "servers": [
            {"url": "https://stag.example.com", "description": "Staging environment"},
            {
                "url": "https://prod.example.com",
                "description": "Production environment",
            },
        ],
        "paths": {
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
            }
        },
        "components": {
            "schemas": {
                "Gif": {
                    "properties": {
                        "id": {"type": "string", "title": "Id"},
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

    json.dumps(tools, cls=JSONEncoder)


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
