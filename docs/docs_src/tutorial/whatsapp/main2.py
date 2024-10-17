import os
from pathlib import Path
from typing import Any

from autogen.agentchat import ConversableAgent, UserProxyAgent

from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

with (Path(__file__).parent / "../../../../examples/openapi/whatsapp_openapi.json").open() as f:
    openapi_json = f.read()

whatsapp_api = OpenAPI.create(
    openapi_json=openapi_json,
)

whatsapp_api_key = "App " # pragma: allowlist secret
whatsapp_api_key += os.getenv("WHATSAPP_API_KEY", "")
whatsapp_api.set_security_params(APIKeyHeader.Parameters(value=whatsapp_api_key))


def is_termination_msg(msg: dict[str, Any]) -> bool:
    return msg["content"] is not None and "TERMINATE" in msg["content"]


user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    is_termination_msg=is_termination_msg,
)

WHATSAPP_SYSTEM_MESSAGE = """Msg Body must be InfobipwhatsappstandaloneapiserviceOpenapiTextMessage e.g.:
{
    "from": "senderNumber",
    "to": "receiverNumber}}",
    "messageId": "test-message-randomInt",
    "content": {
        "text": "message"
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

whatsapp_api._register_for_llm(whatsapp_agent)
whatsapp_api._register_for_execution(user_proxy)

# chat_result = user_proxy.initiate_chat(
#     whatsapp_agent,
#     message="Users initial message: Sender number is 447860099299, receiver is  385911554755 send Hello",
#     summary_method="reflection_with_llm",
#     max_turns=4,
# )
