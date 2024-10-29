from pathlib import Path
from unittest.mock import MagicMock, patch

from autogen import UserProxyAgent

from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader


@patch("fastagency.api.openapi.client.requests.post")
def test_real_whatsapp_end2end(
    mock_post: MagicMock,
) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response

    # file_name = "whatsapp.json"
    file_name = "whatsapp_simple.json"
    # file_name = "whatsapp_openapi_complete.json"

    file_path = (
        Path(__file__).parent.parent.parent.parent / f"examples/openapi/{file_name}"
    )

    with file_path.open(encoding="utf-8") as file:
        openapi_json = file.read()

    api = OpenAPI.create(openapi_json=openapi_json)

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
