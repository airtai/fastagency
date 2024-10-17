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

with (Path(__file__).parent / "../../../../examples/openapi/whatsapp_openapi.json").open() as f:
    openapi_json = f.read()

whatsapp_api_key = os.getenv("WHATSAPP_API_KEY", "")

whatsapp_api = OpenAPI.create(
    openapi_json=openapi_json,
)
whatsapp_api.set_security_params(APIKeyHeader.Parameters(value=whatsapp_api_key))


def is_termination_msg(msg: dict[str, Any]) -> bool:
    return msg["content"] is not None and "TERMINATE" in msg["content"]


user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    is_termination_msg=is_termination_msg,
)

WHATSAPP_SYSTEM_MESSAGE = """Msg Body must be InfobipwhatsappstandaloneapiserviceOpenapiTextMessage"""
whatsapp_agent = ConversableAgent(
    name="Whatsapp_Agent",
    system_message=WHATSAPP_SYSTEM_MESSAGE,
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=is_termination_msg,
)

# wf.register_api(
#     api=whatsapp_api,
#     callers=whatsapp_agent,
#     executors=user_proxy,
# )
whatsapp_api._register_for_llm(whatsapp_agent)
whatsapp_api._register_for_execution(user_proxy)

initial_message = "Sender number is 447860099299, receiver is  385911554755 send Hello"

try:
    chat_result = user_proxy.initiate_chat(
        whatsapp_agent,
        message=f"Users initial message: {initial_message}",
        summary_method="reflection_with_llm",
        max_turns=4,
    )
except Exception as e:
    print(f"Error: {e}")
