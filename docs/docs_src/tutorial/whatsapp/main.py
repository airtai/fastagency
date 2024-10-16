import os
from pathlib import Path
from typing import Any

from autogen.agentchat import ConversableAgent, UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.autogen.autogen import AutoGenWorkflows
from fastagency.ui.console import ConsoleUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

with open(Path("../../../../examples/openapi/whatsapp_openapi.json")) as f:
    openapi_json = f.read()

# infobip_base_url = os.getenv("INFOBIP_BASE_URL", "")
whatsapp_api_key = os.getenv("WHATSAPP_API_KEY", "")

whatsapp_api = OpenAPI.create(
    openapi_json=openapi_json, client_source_path="examples/whatsapp_debug"
)
whatsapp_api.set_security_params(APIKeyHeader.Parameters(value=whatsapp_api_key))


def is_termination_msg(msg: dict[str, Any]) -> bool:
    return msg["content"] is not None and "TERMINATE" in msg["content"]


wf = AutoGenWorkflows()


@wf.register(name="giphy_and_websurfer", description="Giphy and Websurfer chat")
def giphy_workflow_with_security(ui: UI, params: dict[str, Any]) -> str:
    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    WHATSAPP_SYSTEM_MESSAGE = """Msg Body should look like this:
{
    "from": "senderNumber",
    "to": "recipientNumber",
    "messageId": "test-message-random-id",
    "content": {
        "text":
    },
    "callbackData": "Callback data"
}"""
    whatsapp_agent = ConversableAgent(
        name="Whatsapp_Agent",
        system_message=WHATSAPP_SYSTEM_MESSAGE,
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    wf.register_api(
        api=whatsapp_api,
        callers=whatsapp_agent,
        executors=user_proxy,
    )

    print(whatsapp_agent.llm_config["tools"])

    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you send a message to a WhatsApp number. What message would you like to send?",
    )

    chat_result = user_proxy.initiate_chat(
        whatsapp_agent,
        message=f"Users initial message: {initial_message}",
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI(), title="Giphy and Websurfer chat")


[
    {
        "type": "function",
        "function": {
            "description": "Send a text message to a single recipient. Text messages can only be successfully delivered, if the recipient has contacted the business within the last 24 hours, otherwise template message should be used.",
            "name": "channels_whatsapp_send_whatsapp_text_message",
            "parameters": {
                "type": "object",
                "properties": {
                    "body": {
                        "$defs": {
                            "InfobipwhatsappstandaloneapiserviceOpenapiTextContent": {
                                "properties": {
                                    "text": {
                                        "description": "Text of the message that will be sent.",
                                        "maxLength": 4096,
                                        "minLength": 1,
                                        "title": "Text",
                                        "type": "string",
                                    },
                                    "previewUrl": {
                                        "anyOf": [
                                            {"type": "boolean"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "Allows for URL previews in text messages. If the value is set to `true`, text is expected to contain URL starting with `https://` or `http://`. The default value is `false`.",
                                        "title": "Previewurl",
                                    },
                                },
                                "required": ["text"],
                                "title": "InfobipwhatsappstandaloneapiserviceOpenapiTextContent",
                                "type": "object",
                            }
                        },
                        "properties": {
                            "from": {
                                "description": "Registered WhatsApp sender number. Must be in international format.",
                                "maxLength": 24,
                                "minLength": 1,
                                "title": "From",
                                "type": "string",
                            },
                            "to": {
                                "description": "Message recipient number. Must be in international format.",
                                "maxLength": 24,
                                "minLength": 1,
                                "title": "To",
                                "type": "string",
                            },
                            "messageId": {
                                "anyOf": [
                                    {"maxLength": 50, "minLength": 0, "type": "string"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "description": "The ID that uniquely identifies the message sent.",
                                "title": "Messageid",
                            },
                            "content": {
                                "$ref": "#/$defs/InfobipwhatsappstandaloneapiserviceOpenapiTextContent"
                            },
                            "callbackData": {
                                "anyOf": [
                                    {
                                        "maxLength": 4000,
                                        "minLength": 0,
                                        "type": "string",
                                    },
                                    {"type": "null"},
                                ],
                                "default": None,
                                "description": "Custom client data that will be included in Delivery Report.",
                                "title": "Callbackdata",
                            },
                        },
                        "required": ["from", "to", "content"],
                        "title": "InfobipwhatsappstandaloneapiserviceOpenapiTextMessage",
                        "type": "object",
                        "description": "body",
                    }
                },
                "required": ["body"],
            },
        },
    }
]
