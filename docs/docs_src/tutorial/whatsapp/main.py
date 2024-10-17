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

# infobip_base_url = os.getenv("INFOBIP_BASE_URL", "")
whatsapp_api_key = os.getenv("WHATSAPP_API_KEY", "")

whatsapp_api = OpenAPI.create(
    openapi_json=openapi_json
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
