import json

import pytest
import requests
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery

from fastagency.api.openapi import OpenAPI
from fastagency.api.openapi.security import APIKeyCookie as APIKeyCookieSecurity
from fastagency.api.openapi.security import APIKeyHeader as APIKeyHeaderSecurity
from fastagency.api.openapi.security import APIKeyQuery as APIKeyQuerySecurity
from fastagency.api.openapi.security import BaseSecurity


def create_api_key_header_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="OAuth2",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    api_key_header = APIKeyHeader(name="X-API-Key")

    @app.get("/hello")
    def get_hello(api_key_header: str = Security(api_key_header)) -> dict[str, str]:
        if api_key_header == "api_key":  # pragma: allowlist secret
            return {"message": "Hi!"}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return app


def create_api_key_cookie_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="OAuth2",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    api_key_cookie = APIKeyCookie(name="X-API-Key")

    @app.get("/hello")
    def get_hello(api_key_cookie: str = Security(api_key_cookie)) -> dict[str, str]:
        if api_key_cookie == "api_key":  # pragma: allowlist secret
            return {"message": "Hi!"}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return app


def create_api_key_query_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="OAuth2",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    api_key_query = APIKeyQuery(name="X-API-Key")

    @app.get("/hello")
    def get_hello(api_key_query: str = Security(api_key_query)) -> dict[str, str]:
        if api_key_query == "api_key":  # pragma: allowlist secret
            return {"message": "Hi!"}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return app


@pytest.mark.parametrize(
    "fastapi_openapi_url, schema, in_",  # noqa: PT006
    [
        (create_api_key_header_fastapi_app, "APIKeyHeader", "header"),
        (create_api_key_cookie_fastapi_app, "APIKeyCookie", "cookie"),
        (create_api_key_query_fastapi_app, "APIKeyQuery", "query"),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_openapi_schema(
    fastapi_openapi_url: str,
    schema: str,
    in_: str,
) -> None:
    with requests.get(fastapi_openapi_url, timeout=10) as response:
        response.raise_for_status()
        openapi_json = json.loads(response.text)

        expected_schema = {
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
                        "security": [{f"{schema}": []}],
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    f"{schema}": {"type": "apiKey", "in": f"{in_}", "name": "X-API-Key"}
                }
            },
        }

        assert openapi_json == expected_schema


@pytest.mark.parametrize(
    "fastapi_openapi_url, security_class",  # noqa: PT006
    [
        (create_api_key_header_fastapi_app, APIKeyHeaderSecurity),
        (create_api_key_cookie_fastapi_app, APIKeyCookieSecurity),
        (create_api_key_query_fastapi_app, APIKeyQuerySecurity),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_api_key_correct(
    fastapi_openapi_url: str, security_class: BaseSecurity
) -> None:
    api_client = OpenAPI.create(openapi_url=fastapi_openapi_url)
    api_client.set_security_params(security_class.Parameters(value="api_key"))  # type: ignore

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    response = hello_get_f()

    assert response == {"message": "Hi!"}


@pytest.mark.parametrize(
    "fastapi_openapi_url, security_class",  # noqa: PT006
    [
        (create_api_key_header_fastapi_app, APIKeyHeaderSecurity),
        (create_api_key_cookie_fastapi_app, APIKeyCookieSecurity),
        (create_api_key_query_fastapi_app, APIKeyQuerySecurity),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_api_key_wrong(fastapi_openapi_url: str, security_class: BaseSecurity) -> None:
    api_client = OpenAPI.create(openapi_url=fastapi_openapi_url)
    api_client.set_security_params(security_class.Parameters(value="wrong_api_key"))  # type: ignore

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    assert hello_get_f() == {"detail": "Forbidden"}
