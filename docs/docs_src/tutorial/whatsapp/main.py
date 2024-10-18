import os
from pathlib import Path
from typing import Any

from autogen.agentchat import ConversableAgent, UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.autogen.autogen import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

whatsapp_openapi_path = Path(__file__).parent / "../../../../examples/openapi/whatsapp_openapi.json"
with whatsapp_openapi_path.open() as f:
    openapi_json = f.read()

whatsapp_api = OpenAPI.create(
    openapi_json=openapi_json,
)

whatsapp_api_key = "App " # pragma: allowlist secret
whatsapp_api_key += os.getenv("WHATSAPP_API_KEY", "")
whatsapp_api.set_security_params(APIKeyHeader.Parameters(value=whatsapp_api_key))

wf = AutoGenWorkflows()

@wf.register(name="whatsapp", description="WhatsApp chat")
def whatsapp_workflow(ui: UI, params: dict[str, Any]) -> str:
    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    WHATSAPP_SYSTEM_MESSAGE = """Msg Body must use the following format:
{
    "from": "447860099299",
    "to": "receiverNumber",
    "messageId": "test-message-randomInt",
    "content": {
        "text": "message"
    },
    "callbackData": "Callback data"
}

"from" number is always the same.
"""
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

    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="""I can help you send a message to your WhatsApp.
What is your number and which message would you like to send?""",
    )

    chat_result = user_proxy.initiate_chat(
        whatsapp_agent,
        message=f"Users initial message: {initial_message}",
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=MesopUI(), title="WhatsApp chat")
