import os

from autogen.agentchat import ConversableAgent, UserProxyAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtime.autogen.base import AutoGenWorkflows
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


@wf.register(name="weatherman_workflow", description="Weatherman chat")
def simple_workflow(
    wf: AutoGenWorkflows, ui: UI, initial_message: str, session_id: str
) -> str:
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

    chat_result = user_proxy.initiate_chat(
        weatherman,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary


app = FastAgency(wf=wf, ui=ConsoleUI())
