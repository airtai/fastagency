import json
from typing import Annotated

import pytest
import requests
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from docs.docs_src.user_guide.external_rest_apis.security_examples import (
    configure_http_basic_client,
)


def create_http_basic_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="OAuth2",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    security = HTTPBasic()

    # Dependency to verify the username/password
    def verify_auth(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    ) -> None:
        if (credentials.username != "john") or (
            credentials.password != "supersecret"  # pragma: allowlist secret
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid username or password",
            )

    # Secured endpoint
    @app.get("/hello")
    def get_hello(
        credentials: HTTPBasicCredentials = Depends(verify_auth),  # noqa: B008
    ) -> dict[str, str]:
        return {"message": "Hello, authenticated user!"}

    return app


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_http_basic_fastapi_app)],
    indirect=["fastapi_openapi_url"],
)
def test_openapi_schema(fastapi_openapi_url: str) -> None:
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
                    "security": [{"HTTPBasic": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {"HTTPBasic": {"type": "http", "scheme": "basic"}}
        },
    }

    assert openapi_json == expected_schema


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [
        (create_http_basic_fastapi_app),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_http_bearer_token_correct(fastapi_openapi_url: str) -> None:
    api_client = configure_http_basic_client(
        fastapi_openapi_url,
        username="john",
        password="supersecret",  # pragma: allowlist secret
    )

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
        (create_http_basic_fastapi_app),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_http_bearer_token_wrong(fastapi_openapi_url: str) -> None:
    api_client = configure_http_basic_client(
        fastapi_openapi_url,
        username="john",
        password="wrongsecret",  # pragma: allowlist secret
    )

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    assert hello_get_f() == {"detail": "Invalid username or password"}
