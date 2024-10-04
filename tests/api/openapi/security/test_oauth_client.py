import json
from typing import Annotated, Any

import pytest
import requests
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer as FastAPIOAuth2PasswordBearer

from fastagency.api.openapi import OpenAPI
from fastagency.api.openapi.security import OAuth2PasswordBearer


def create_oauth2_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="OAuth2",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    oauth2_scheme = FastAPIOAuth2PasswordBearer(tokenUrl="token")

    @app.post("/low", summary="Low Level")
    async def post_oauth(
        message: str, token: Annotated[str, Depends(oauth2_scheme)]
    ) -> dict[str, str]:
        if token != "token123":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"message": message}

    return app


@pytest.fixture
def openapi_oauth2_schema() -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {"title": "OAuth2", "version": "0.1.0"},
        "servers": [
            {"url": "http://127.0.0.1:43465", "description": "Local development server"}
        ],
        "paths": {
            "/low": {
                "post": {
                    "summary": "Low Level",
                    "operationId": "post_oauth_low_post",
                    "security": [{"OAuth2PasswordBearer": []}],
                    "parameters": [
                        {
                            "name": "message",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string", "title": "Message"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "additionalProperties": {"type": "string"},
                                        "title": "Response Post Oauth Low Post",
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
            },
            "securitySchemes": {
                "OAuth2PasswordBearer": {
                    "type": "oauth2",
                    "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
                }
            },
        },
    }


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_oauth2_fastapi_app)],
    indirect=["fastapi_openapi_url"],
)
def test_oauth2_fastapi_app(
    fastapi_openapi_url: str, openapi_oauth2_schema: dict[str, Any]
) -> None:
    with requests.get(fastapi_openapi_url, timeout=10) as response:
        response.raise_for_status()
        openapi_json = json.loads(response.text)

    openapi_oauth2_schema.pop("servers")
    servers = openapi_json.pop("servers")

    assert servers[0]["url"] == fastapi_openapi_url.split("/openapi.json")[0]
    assert openapi_oauth2_schema == openapi_json


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_oauth2_fastapi_app)],
    indirect=["fastapi_openapi_url"],
)
def test_generate_oauth2_client(fastapi_openapi_url: str) -> None:
    api_client = OpenAPI.create(openapi_url=fastapi_openapi_url)
    api_client.set_security_params(
        OAuth2PasswordBearer.Parameters(bearer_token="token123")
    )

    expected = ["post_oauth_low_post"]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    post_oauth_f = functions[0]

    response = post_oauth_f(message="message")

    assert response == {"message": "message"}
