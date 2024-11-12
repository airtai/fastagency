import json

import pytest

from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import HTTPBearer, UnsuportedSecurityStub

from .test_http_bearer_client import create_http_bearer_fastapi_app


@pytest.fixture
def openapi_schema_with_unsupported_security(fastapi_openapi_url: str) -> str:
    return json.dumps(
        {
            "openapi": "3.1.0",
            "info": {"title": "OAuth2", "version": "0.1.0"},
            "servers": [
                {
                    "url": f"{fastapi_openapi_url.split('/openapi.json')[0]}",
                    "description": "Local development server",
                }
            ],
            "paths": {
                "/hello": {
                    "get": {
                        "summary": "Get Hello",
                        "operationId": "get_hello_hello_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "additionalProperties": {"type": "string"},
                                            "type": "object",
                                            "title": "Response Get Hello Hello Get",
                                        }
                                    }
                                },
                            }
                        },
                        "security": [
                            {"HTTPBearer": [], "Non-existent": []},
                        ],
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    "HTTPBearer": {"type": "http", "scheme": "bearer"},
                    "Non-existent": {"type": "non-existent"},
                }
            },
        }
    )


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [
        (create_http_bearer_fastapi_app),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_http_bearer_token_correct(
    fastapi_openapi_url: str, openapi_schema_with_unsupported_security: str
) -> None:
    api_client = OpenAPI.create(openapi_json=openapi_schema_with_unsupported_security)
    api_client.set_security_params(HTTPBearer.Parameters(value="supersecret"))

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    response = hello_get_f()

    assert response == {"message": "Hello, authenticated user!"}


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [
        (create_http_bearer_fastapi_app),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_setting_parameters_on_stub(
    fastapi_openapi_url: str, openapi_schema_with_unsupported_security: str
) -> None:
    api_client = OpenAPI.create(openapi_json=openapi_schema_with_unsupported_security)
    with pytest.raises(RuntimeError) as e:
        api_client.set_security_params(
            UnsuportedSecurityStub.Parameters(value="supersecret"),
            name="get_hello_hello_get",
        )

    assert str(e.value) == "Trying to set UnsuportedSecurityStub params"
