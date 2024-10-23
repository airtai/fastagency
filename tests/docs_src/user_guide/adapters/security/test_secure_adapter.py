import json

import pytest
import requests
import websockets
from dirty_equals import IsPartialDict
from fastapi import FastAPI

from docs.docs_src.user_guide.adapters.fastapi.security.main_1_jwt import app as app_jwt
from docs.docs_src.user_guide.adapters.fastapi.security.main_1_simple import (
    app as app_simple,
)


def create_oauth2_fastapi_app_simple(host: str, port: int) -> FastAPI:
    app_simple.servers = [
        {"url": f"http://{host}:{port}", "description": "Local development server"}
    ]
    return app_simple


def create_oauth2_fastapi_app_jwt(host: str, port: int) -> FastAPI:
    app_jwt.servers = [
        {"url": f"http://{host}:{port}", "description": "Local development server"}
    ]
    return app_jwt


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_oauth2_fastapi_app_simple), (create_oauth2_fastapi_app_jwt)],
    indirect=["fastapi_openapi_url"],
)
def test_secure_unauthorized(
    fastapi_openapi_url: str,
) -> None:
    fastagency_url = fastapi_openapi_url.split("/openapi.json")[0]

    initiate_workflow_response = requests.post(
        fastagency_url + "/fastagency/initiate_workflow"
    )
    assert initiate_workflow_response.status_code == 401

    discovery_response = requests.get(fastagency_url + "/fastagency/discovery")
    assert discovery_response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_oauth2_fastapi_app_simple), (create_oauth2_fastapi_app_jwt)],
    indirect=["fastapi_openapi_url"],
)
async def test_secure_unauthorized_websocket(
    fastapi_openapi_url: str,
) -> None:
    fastagency_url = fastapi_openapi_url.split("/openapi.json")[0]

    connect_url = f"ws{fastagency_url[4:]}/fastagency/ws"

    with pytest.raises(websockets.legacy.exceptions.InvalidStatusCode) as e:
        async with websockets.connect(connect_url):
            pass

    assert e.value.status_code == 401


@pytest.fixture
def token(fastapi_openapi_url: str) -> str:
    auth_url = f"{fastapi_openapi_url.split('/openapi.json')[0]}/token"

    response = requests.post(
        auth_url,
        data={
            "username": "johndoe",
            "password": "secret",  # pragma: allowlist secret
        },
    )

    token = response.json().get("access_token")
    return token  # type: ignore


@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_oauth2_fastapi_app_simple), (create_oauth2_fastapi_app_jwt)],
    indirect=["fastapi_openapi_url"],
)
def test_secure_authorized(
    fastapi_openapi_url: str,
    token: str,
) -> None:
    fastagency_url = fastapi_openapi_url.split("/openapi.json")[0]

    payload = {
        "workflow_name": "simple_learning",
        "workflow_uuid": "1234",
        "user_id": None,
        "params": {"message": "Hello"},
    }

    initiate_workflow_response = requests.post(
        fastagency_url + "/fastagency/initiate_workflow",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    assert initiate_workflow_response.status_code == 200

    discovery_response = requests.get(
        fastagency_url + "/fastagency/discovery",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert discovery_response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_oauth2_fastapi_app_simple), (create_oauth2_fastapi_app_jwt)],
    indirect=["fastapi_openapi_url"],
)
async def test_secure_authorized_websocket(
    fastapi_openapi_url: str,
    token: str,
) -> None:
    fastagency_url = fastapi_openapi_url.split("/openapi.json")[0]

    payload = {
        "user_id": "ac4418be-c656-4db8-ada9-b2556b5d1e02",
        "workflow_uuid": "a1ce322f-6fee-4cbf-9eba-49fb0f6b345c",
        "name": "simple_learning",
        "params": {"message": "Hello"},
    }

    connect_url = f"ws{fastagency_url[4:]}/fastagency/ws"

    async with websockets.connect(
        connect_url,
        extra_headers={
            "Authorization": f"Bearer {token}",
        },
    ) as websocket:
        await websocket.send(json.dumps(payload))

        response = await websocket.recv()
        response = response.decode() if isinstance(response, bytes) else response

        expected = {
            "sender": "AutoGenWorkflows",
            "recipient": "User",
            "auto_reply": False,
            "content": {
                "name": "simple_learning",
                "description": "Student and teacher learning chat",
                "params": {"message": "Hello"},
            },
            "type": "workflow_started",
        }

        assert json.loads(response) == IsPartialDict(**expected)
