import os

from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency, Workflows
from fastagency.api.openapi import OpenAPI
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}

WEATHER_OPENAPI_URL = "https://weather.tools.fastagency.ai/openapi.json"

wf = AutoGenWorkflows()


@wf.register(name="simple_weather", description="Weather chat")
def weather_workflow(
    wf: Workflows, ui: UI, initial_message: str, session_id: str
) -> str:
    weather_api = OpenAPI.create(openapi_url=WEATHER_OPENAPI_URL)

    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    weather_agent = ConversableAgent(
        name="Weather_Agent",
        system_message="You are a weather agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    wf.register_api(
        api=weather_api,
        callers=user_agent,
        executors=weather_agent,
    )

    chat_result = user_agent.initiate_chat(
        weather_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(wf=wf, ui=MesopUI())
