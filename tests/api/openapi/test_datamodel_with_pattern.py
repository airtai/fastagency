import json
from typing import Any

import pytest
from fastapi import FastAPI
from pydantic import BaseModel, Field

from fastagency.api.openapi import OpenAPI


def create_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="My app",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    class MyClass(BaseModel):
        """Model of my class."""

        my_field: str = Field(pattern=r"[A-Z]\d{9}")

    @app.post("/my-endpoint")
    def my_endpoint(my_class: MyClass) -> MyClass:
        """My endpoint."""
        return my_class

    return app


@pytest.fixture
def openapi_schema() -> dict[str, Any]:
    app = create_app(host="127.0.0.1", port=8000)

    return app.openapi()


def test_openapi_schema(openapi_schema: dict[str, Any]) -> None:
    expected_schema = {
        "openapi": "3.1.0",
        "info": {"title": "My app", "version": "0.1.0"},
        "servers": [
            {"url": "http://127.0.0.1:8000", "description": "Local development server"}
        ],
        "paths": {
            "/my-endpoint": {
                "post": {
                    "summary": "My Endpoint",
                    "description": "My endpoint.",
                    "operationId": "my_endpoint_my_endpoint_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MyClass"}
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/MyClass"}
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
                "MyClass": {
                    "properties": {
                        "my_field": {
                            "type": "string",
                            "pattern": "[A-Z]\\d{9}",
                            "title": "My Field",
                        }
                    },
                    "type": "object",
                    "required": ["my_field"],
                    "title": "MyClass",
                    "description": "Model of my class.",
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


def test_generate_client(openapi_schema: dict[str, Any]) -> None:
    api_client = OpenAPI.create(
        openapi_json=json.dumps(openapi_schema),
    )

    expected = ["my_endpoint_my_endpoint_post"]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected
