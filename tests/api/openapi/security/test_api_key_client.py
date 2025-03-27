import json
from typing import Callable

import pytest
import requests
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery

from docs.docs_src.user_guide.external_rest_apis.security_examples import (
    configure_api_key_cookie_client,
    configure_api_key_header_client,
    configure_api_key_query_client,
)
from fastagency.api.openapi import OpenAPI


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


@pytest.mark.skip(reason="fastagency.api.openapi.OpenAPI is not implemented yet.")
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


@pytest.mark.skip(reason="fastagency.api.openapi.OpenAPI is not implemented yet.")
@pytest.mark.parametrize(
    "fastapi_openapi_url, client_config_func",  # noqa: PT006
    [
        (create_api_key_header_fastapi_app, configure_api_key_header_client),
        (create_api_key_cookie_fastapi_app, configure_api_key_cookie_client),
        (create_api_key_query_fastapi_app, configure_api_key_query_client),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_api_key_correct(
    fastapi_openapi_url: str,
    client_config_func: Callable[OpenAPI, dict[str, str]],  # type: ignore
) -> None:
    api_client = client_config_func(fastapi_openapi_url, "api_key")  # type: ignore

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    response = hello_get_f()

    assert response == {"message": "Hi!"}


@pytest.mark.skip(reason="fastagency.api.openapi.OpenAPI is not implemented yet.")
@pytest.mark.parametrize(
    "fastapi_openapi_url, client_config_func",  # noqa: PT006
    [
        (create_api_key_header_fastapi_app, configure_api_key_header_client),
        (create_api_key_cookie_fastapi_app, configure_api_key_cookie_client),
        (create_api_key_query_fastapi_app, configure_api_key_query_client),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_api_key_wrong(
    fastapi_openapi_url: str,
    client_config_func: Callable[OpenAPI, dict[str, str]],  # type: ignore
) -> None:
    api_client = client_config_func(fastapi_openapi_url, "wrong_api_key")  # type: ignore

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    assert hello_get_f() == {"detail": "Forbidden"}
