import os
from typing import Any

from autogen import UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.runtimes.ag2 import Workflow
from fastagency.runtimes.ag2.agents.whatsapp import WhatsAppAgent
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

wf = Workflow()


@wf.register(name="simple_whatsapp", description="WhatsApp chat")  # type: ignore[type-var]
def whatsapp_workflow(ui: UI, params: dict[str, Any]) -> str:
    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you with sending a message over whatsapp, what would you like to send?",
    )
    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent, when the message is successfully sent, you can end the conversation by sending 'TERMINATE'",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    whatsapp_agent = WhatsAppAgent(
        name="Assistant_Agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
        executor=user_agent,
        # This is the default sender number for Infobip.
        # If you want to use your own sender, please update the value below:
        sender="447860099299",
        whatsapp_api_key=os.getenv("WHATSAPP_API_KEY", ""),
        is_termination_msg=is_termination_msg,
    )

    run_response = user_agent.run(
        whatsapp_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )

    return run_response.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
