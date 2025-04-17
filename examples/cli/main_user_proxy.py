import os
from typing import Any

from autogen import ConversableAgent, LLMConfig, UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.ag2 import Workflow
from fastagency.ui.console import ConsoleUI

llm_config = LLMConfig(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.8,
)


wf = Workflow()


@wf.register(name="weatherman_workflow", description="Weatherman chat")
def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
    with llm_config:
        user_proxy = UserProxyAgent(
            name="User_Proxy",
            human_input_mode="ALWAYS",
        )
        weatherman = ConversableAgent(
            name="Weatherman",
            system_message="You are a weatherman.",
        )

    weather_client = OpenAPI.create(
        openapi_url="https://weather.tools.fastagency.ai/openapi.json"
    )
    # Set global security params for all methods
    weather_client.set_security_params(
        APIKeyHeader.Parameters(value="secure weather key")
    )

    wf.register_api(
        api=weather_client,
        callers=user_proxy,
        executors=weatherman,
    )

    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="What would you like to find out about weather?",
    )

    response = user_proxy.run(
        weatherman,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return ui.process(response)


app = FastAgency(provider=wf, ui=ConsoleUI())
