import os
from typing import Annotated, Any, Literal

from autogen import register_function
from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.api.code_injection import inject_params
from fastagency.runtimes.autogen import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI

erste_tokens_amount_dict = {
    "token-1-c": 100,
    "token-1-f": 200,
}

rba_tokens_amount_dict = {
    "token-1-a": 1_000,
    "token-1-b": 20_000,
    "token-2-a": -200,
}

bank_tokens_amount_dict = {
    "erste": erste_tokens_amount_dict,
    "rba": rba_tokens_amount_dict,
}

def get_savings(bank: Annotated[Literal["erste", "rba"], "Bank name: 'erste' or 'rba'"], token: Annotated[str, "Token"]) -> str:
    if token not in bank_tokens_amount_dict[bank]:
        raise ValueError("Token not found")
    return f"Your savings: {bank_tokens_amount_dict[bank][token]}$"


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

@wf.register(name="simple_weather", description="Weather chat")
def weather_workflow(
    ui: UI, params: dict[str, str]
) -> str:
    bank = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="Enter your bank",
    )
    token = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="Enter your token",
    )

    ctx: dict[str, Any] = {"token": token}
    get_savings_with_params = inject_params(get_savings, ctx)

    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    banker_agent = ConversableAgent(
        name="Banker_Agent",
        system_message="You are a banker agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    register_function(
        f=get_savings_with_params,
        caller=banker_agent,
        executor=user_agent,
        description="Get savings",
    )

    initial_message = f"We need to get user's savings for {bank}"
    chat_result = user_agent.initiate_chat(
        banker_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=MesopUI())
