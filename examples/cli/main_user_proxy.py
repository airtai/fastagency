import os
from typing import Any

from autogen.agentchat import ConversableAgent, UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.autogen import AutoGenWorkflows
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


@wf.register(name="weatherman_workflow", description="Weatherman chat")
def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="ALWAYS",
        llm_config=llm_config,
    )
    weatherman = ConversableAgent(
        name="Weatherman",
        system_message="You are a weatherman.",
        llm_config=llm_config,
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

    chat_result = user_proxy.initiate_chat(
        weatherman,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary


app = FastAgency(provider=wf, ui=ConsoleUI())
