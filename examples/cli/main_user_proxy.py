import os

from autogen.agentchat import ConversableAgent, UserProxyAgent

from fastagency.core import Chatable
from fastagency.core.io.console import ConsoleIO
from fastagency.core.runtimes.autogen.base import AutoGenWorkflows
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader

from fastagency import FastAgency

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
def simple_workflow(io: Chatable, initial_message: str, session_id: str) -> str:

    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="ALWAYS",
    )
    weatherman = ConversableAgent(
        name="Weatherman",
        system_message="You are a weatherman.",
        llm_config=llm_config,
    )

    weather_client = OpenAPI.create(openapi_url="https://weather.tools.fastagency.ai/openapi.json")
    # Set global security params for all methods
    weather_client.set_security_params(APIKeyHeader.Parameters(value="secure weather key"))

    weather_client.register_for_llm(weatherman)
    weather_client.register_for_execution(user_proxy)

    chat_result = user_proxy.initiate_chat(
        weatherman,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )

    return chat_result.summary

app = FastAgency(wf=wf, io=ConsoleIO())
