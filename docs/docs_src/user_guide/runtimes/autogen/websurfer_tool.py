import os
from typing import Any

from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.runtimes.autogen import AutoGenWorkflows
from fastagency.runtimes.autogen.tools import WebSurferTool
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

wf = AutoGenWorkflows()


@wf.register(name="simple_websurfer", description="WebSurfer chat")  # type: ignore[type-var]
def websurfer_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you with your web search. What would you like to know?",
    )

    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    assistant_agent = ConversableAgent(
        name="Assistant_Agent",
        system_message="You are a useful assistant",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    web_surfer = WebSurferTool(
        name_prefix="Web_Surfer",
        llm_config=llm_config,
        summarizer_llm_config=llm_config,
    )

    web_surfer.register(
        caller=assistant_agent,
        executor=user_agent,
    )

    chat_result = user_agent.initiate_chat(
        assistant_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
