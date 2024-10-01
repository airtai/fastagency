import os
from typing import Annotated, Any, Optional

from autogen import register_function
from autogen import ConversableAgent, UserProxyAgent

from fastagency import UI, FastAgency, Workflows
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyQuery
from fastagency.base import MultipleChoice
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI


llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}

openapi_url = "https://raw.githubusercontent.com/airtai/fastagency/refs/heads/main/examples/openapi/giphy_openapi.json"
giphy_api = OpenAPI.create(openapi_url=openapi_url)

giphy_api_key = os.getenv("GIPHY_API_KEY")
giphy_api.set_security_params(APIKeyQuery.Parameters(value=giphy_api_key))

wf = AutoGenWorkflows()


@wf.register(name="giphy_and_websurfer", description="Giphy and Websurfer chat")
def giphy_workflow_with_security(
    wf: Workflows, ui: UI, initial_message: str, session_id: str
) -> str:
    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="ALWAYS",
        is_termination_msg=is_termination_msg,
    )

    giphy_agent = ConversableAgent(
        name="Giphy_Agent",
        system_message="You are a helper agent that communicates with the user and Giphy API. When using API, always limit the response size to 5 items. Write 'TERMINATE' to end the conversation.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )
    wf.register_api(
        api=giphy_api,
        callers=giphy_agent,
        executors=user_proxy,
        functions=["random_gif", "search_gifs", "trending_gifs"],
    )

    chat_result = user_proxy.initiate_chat(
        giphy_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(wf=wf, ui=MesopUI(), title="Giphy chat")
