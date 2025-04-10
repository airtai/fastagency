import os
from typing import Any

from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi import OpenAPI
from fastagency.runtimes.ag2 import Workflow
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

openapi_url = "https://weather.tools.fastagency.ai/openapi.json"

weather_api = OpenAPI.create(openapi_url=openapi_url)

weather_agent_system_message = """You are a weather agent. When asked
for weather, always call the function to get real-time data immediately.
Do not respond until the data is retrieved. Provide the actual weather
concisely based only on the real-time data from the function. Do not
use any pre-existing knowledge or memory."""

wf = Workflow()


@wf.register(name="simple_weather", description="Weather chat")  # type: ignore[type-var]
def weather_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you with the weather. What would you like to know?",
    )

    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
        code_execution_config=False
    )
    weather_agent = ConversableAgent(
        name="Weather_Agent",
        system_message=weather_agent_system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    wf.register_api(  # type: ignore[attr-defined]
        api=weather_api,
        callers=[user_agent],
        executors=[weather_agent],
        functions=[
            {
                "get_daily_weather_daily_get": {
                    "name": "get_daily_weather",
                    "description": "Get the daily weather",
                }
            },
            "get_hourly_weather_hourly_get",
        ],
    )

    response = user_agent.run(
        weather_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return ui.process(response)  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=MesopUI())
