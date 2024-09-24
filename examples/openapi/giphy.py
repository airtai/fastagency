# import json
import os

# from pathlib import Path
from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency, Workflows
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyQuery
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.console import ConsoleUI

# with Path("giphy_openapi.json").open() as f:
#     data = json.load(f)
#     openapi_json = json.dumps(data, indent=2)

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}

# giphy_api = OpenAPI.create(openapi_json=openapi_json)
openapi_url = "https://raw.githubusercontent.com/airtai/fastagency/refs/heads/main/examples/openapi/giphy_openapi.json"
giphy_api = OpenAPI.create(openapi_url=openapi_url)
giphy_api_key = os.getenv("GIPHY_API_KEY")
# print(f"API Key is {giphy_api_key}")

giphy_api.set_security_params(APIKeyQuery.Parameters(value=giphy_api_key))


wf = AutoGenWorkflows()


@wf.register(name="giphy_with_security", description="Giphy chat with security")
def giphy_workflow_with_security(
    wf: Workflows, ui: UI, initial_message: str, session_id: str
) -> str:
    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    giphy_agent = ConversableAgent(
        name="Giphy_Agent",
        system_message="You are a giphy API agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    functions = ["random_gif", "search_gifs", "trending_gifs"]
    wf.register_api(
        api=giphy_api,
        callers=giphy_agent,
        executors=user_agent,
        functions=functions,
    )

    chat_result = user_agent.initiate_chat(
        giphy_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(wf=wf, ui=ConsoleUI())
