from os import environ
from unittest.mock import MagicMock, patch
from pathlib import Path

import pytest
import requests
from autogen import UserProxyAgent

from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader


@pytest.fixture(scope="session")
def whatsapp_api_schema() -> str:
    postman_api_key = environ.get("POSTMAN_API_KEY")
    api_id = "348d2a2f-42dc-4e65-86c7-7c4b589a0693"
    url = f"https://api.getpostman.com/apis/{api_id}"

    # Define the headers for authentication
    headers = {"X-Api-Key": postman_api_key}

    # Make the GET request to download the collection
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    api_data = response.json()

    return api_data["api"]["versions"][0]["schemas"][0]["content"]  # type: ignore [no-any-return]


@pytest.mark.postman
@patch("fastagency.api.openapi.client.requests.post")
def test_real_whatsapp_end2end(
    mock_post: MagicMock,
    whatsapp_api_schema: str,
) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response

    # file_name = "whatsapp_simple.json"

    # file_path = (
    #     Path(__file__).parent.parent.parent.parent / f"examples/openapi/{file_name}"
    # )

    # with file_path.open(encoding="utf-8") as file:
    #     openapi_json = file.read()

    # api = OpenAPI.create(
    #     openapi_json=openapi_json,
    #     client_source_path=".",
    # )

    api = OpenAPI.create(
        openapi_json=whatsapp_api_schema,
        servers=[{"url": "https://api.infobip.com"}],
    )

    assert isinstance(api, OpenAPI)

    header_authorization = "App something"  # pragma: allowlist secret
    api.set_security_params(APIKeyHeader.Parameters(value=header_authorization))

    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    functions = ["channels_whatsapp_send_whatsapp_text_message"]
    api._register_for_execution(user_proxy, functions=functions)

    assert tuple(user_proxy._function_map.keys()) == (
        "channels_whatsapp_send_whatsapp_text_message",
    )

    channels_whatsapp_send_whatsapp_text_message = user_proxy._function_map[
        "channels_whatsapp_send_whatsapp_text_message"
    ]

    channels_whatsapp_send_whatsapp_text_message(
        **{
            "body": {
                "from": "447860099299",
                "to": "38591152131",
                "messageId": "test-message-123",
                "content": {"text": "Hello, World!"},
                "callbackData": "Callback data",
            }
        }
    )

    mock_post.assert_called_once_with(
        "https://api.infobip.com/whatsapp/1/message/text",
        params={},
        headers={
            "Authorization": header_authorization,
            "Content-Type": "application/json",
        },
        json={
            "from": "447860099299",
            "to": "38591152131",
            "messageId": "test-message-123",
            "content": {"text": "Hello, World!"},
            "callbackData": "Callback data",
        },
    )


@patch("fastagency.api.openapi.client.requests.post")
def test_real_whatsapp_end2end_problematic(
    mock_post: MagicMock,
) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response

    file_name = "whatsapp_simple.json"

    file_path = (
        Path(__file__).parent.parent.parent.parent / f"examples/openapi/{file_name}"
    )

    with file_path.open(encoding="utf-8") as file:
        openapi_json = file.read()

    api = OpenAPI.create(
        openapi_json=openapi_json,
        client_source_path=".",
    )

    assert isinstance(api, OpenAPI)

    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    functions = ["send_whatsapp_text_message"]
    api._register_for_execution(user_proxy, functions=functions)

    assert tuple(user_proxy._function_map.keys()) == ("send_whatsapp_text_message",)

    send_whatsapp_text_message = user_proxy._function_map["send_whatsapp_text_message"]

    send_whatsapp_text_message(
        **{
            "body": {
                "from": "447860099299",
                "to": "38591152131",
                "messageId": "test-message-123",
                "content": {"text": "Hello, World!"},
                "callbackData": "Callback data",
            }
        }
    )

    mock_post.assert_called_once()

    mock_post.assert_called_once_with(
        "https://api.infobip.com/whatsapp/1/message/text",
        params={},
        headers={
            "Content-Type": "application/json",
        },
        json={
            "from": "447860099299",
            "to": "38591152131",
            "messageId": "test-message-123",
            "content": {"text": "Hello, World!"},
            "callbackData": "Callback data",
        },
    )
