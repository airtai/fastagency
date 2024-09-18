import os
from typing import Annotated

from autogen.agentchat import ConversableAgent, GroupChat, GroupChatManager, UserProxyAgent

from fastagency import UI
from fastagency.ui.console import ConsoleUI
from fastagency.runtime.autogen.base import AutoGenWorkflows

from fastagency import FastAgency

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}


wf = AutoGenWorkflows()

@wf.register(name="plan_and_execute", description="Planning and execution chat")  # type: ignore[type-var]
def simple_workflow(wf: AutoGenWorkflows, ui: UI, initial_message: str, session_id: str) -> str:
    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="ALWAYS",
    )
    planner = ConversableAgent(
        name="Planner",
        system_message="You are a planner responsible for creating a plan on hot to solve a task.",
        llm_config=llm_config,
    )
    controller = ConversableAgent(
        name="Controller",
        system_message="You are a controller responsible for controlling the plan and its execution.",
        llm_config=llm_config,
    )

    @user_proxy.register_for_execution()  # type: ignore[misc]
    @controller.register_for_llm(name="execute_plan", description="Execute the plan")  # type: ignore[misc]
    def execute_plan(plan: Annotated[str, "The plan to execute"]) -> str:
        # todo: create a new groupchat and execute the plan
        inner_user_proxy = UserProxyAgent(
            name="User_Proxy",
            human_input_mode="ALWAYS",
        )
        executor = ConversableAgent(
            name="Executor",
            system_message="You are an executor responsible for executing the plan.",
            llm_config=llm_config,
        )
        @inner_user_proxy.register_for_execution()  # type: ignore[misc]
        @executor.register_for_llm(name="execute_plan", description="Execute the plan")  # type: ignore[misc]
        def some_tool(param: Annotated[str, "Some parameter"]) -> str:
            # todo: write a tool
            ...
            return "result"

        chat_result = inner_user_proxy.initiate_chat(
            executor,
            message=initial_message,
            summary_method="reflection_with_llm",
            max_turns=5,
        )

        return chat_result.summary  # type: ignore[no-any-return]

    groupchat = GroupChat(agents=[user_proxy, planner, controller], messages=[], max_round=12)
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    chat_result = user_proxy.initiate_chat(
        manager,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )

    return chat_result.summary  # type: ignore[no-any-return]

app = FastAgency(wf=wf, ui=ConsoleUI())
