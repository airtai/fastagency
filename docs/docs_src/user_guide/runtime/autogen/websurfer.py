import os

from autogen import UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.runtime.autogen import AutoGenWorkflows
from fastagency.runtime.autogen.agents.websurfer import WebSurferAgent
from fastagency.ui.console import ConsoleUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}

wf = AutoGenWorkflows()

@wf.register(name="simple_websurfer", description="WebSurfer chat")  # type: ignore[type-var]
def websurfer_workflow(
    wf: AutoGenWorkflows, ui: UI, initial_message: str, session_id: str
) -> str:
    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    web_surfer = WebSurferAgent(
        name="Assistant_Agent",
        llm_config=llm_config,
        summarizer_llm_config=llm_config,
        human_input_mode="NEVER",
        executor=user_agent,
    )

    chat_result = user_agent.initiate_chat(
        web_surfer,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
