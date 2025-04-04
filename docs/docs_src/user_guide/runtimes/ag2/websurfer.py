import os
from typing import Any

from autogen import UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.runtimes.ag2 import Workflow
from fastagency.runtimes.ag2.agents.websurfer import WebSurferAgent
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
    web_surfer = WebSurferAgent(
        name="Assistant_Agent",
        llm_config=llm_config,
        summarizer_llm_config=llm_config,
        human_input_mode="NEVER",
        executor=user_agent,
        bing_api_key=os.getenv("BING_API_KEY"),
    )

    run_response = user_agent.run(
        web_surfer,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return run_response.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
