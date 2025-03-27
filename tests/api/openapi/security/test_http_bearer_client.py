import json

import pytest
import requests
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from docs.docs_src.user_guide.external_rest_apis.security_examples import (
    configure_http_bearer_client,
)


def create_http_bearer_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="OAuth2",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    # Create the HTTPBearer object
    bearer_scheme = HTTPBearer()

    # Dependency to verify the token
    def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # noqa: B008
    ) -> None:
        if credentials.credentials != "supersecret":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
            )

    # Secured endpoint
    @app.get("/hello")
    def get_hello(
        credentials: HTTPAuthorizationCredentials = Depends(verify_token),  # noqa: B008
    ) -> dict[str, str]:
        return {"message": "Hello, authenticated user!"}

    return app


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_http_bearer_fastapi_app)],
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
                    "security": [{"HTTPBearer": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {"HTTPBearer": {"type": "http", "scheme": "bearer"}}
        },
    }

    assert openapi_json == expected_schema


@pytest.mark.skip(reason="fastagency.api.openapi.OpenAPI is not implemented yet.")
@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [
        (create_http_bearer_fastapi_app),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_http_bearer_token_correct(fastapi_openapi_url: str) -> None:
    api_client = configure_http_bearer_client(fastapi_openapi_url, "supersecret")

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    response = hello_get_f()

    assert response == {"message": "Hello, authenticated user!"}


@pytest.mark.skip(reason="fastagency.api.openapi.OpenAPI is not implemented yet.")
@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [
        (create_http_bearer_fastapi_app),
    ],
    indirect=["fastapi_openapi_url"],
)
def test_http_bearer_token_wrong(fastapi_openapi_url: str) -> None:
    api_client = configure_http_bearer_client(fastapi_openapi_url, "wrong_api_key")

    expected = [
        "get_hello_hello_get",
    ]

    functions = list(api_client._get_functions_to_register())
    assert [f.__name__ for f in functions] == expected

    hello_get_f = functions[0]

    assert hello_get_f() == {"detail": "Invalid or expired token"}
