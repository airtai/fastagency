import os
from typing import Annotated, Any, Optional

from autogen import register_function
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.runtimes.autogen import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI

wf = AutoGenWorkflows()

@wf.register(name="text_message", description="Text message test")
def many_multiple_choice_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    ui.text_message(
        sender="Workflow",
        recipient="User",
        body="text message body"
    )
    return "Completed OK"  # type: ignore[no-any-return]

@wf.register(name="text_input_message", description="Text input message test")
def multiple_choice_single_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    answer = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="Have you run any tests recently?"
    )
    return answer  # type: ignore[no-any-return]


@wf.register(name="multiple_choice_message_single", description="Multiple choice - single")
def multiple_choice_single_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    answer = ui.multiple_choice(
        sender="Workflow",
        recipient="User",
        prompt="When was the last time you have run automated tests?",
        choices=["I am currently running them", "yesterday", "Tests? What tests??"]
    )
    return f"you have chosen: {answer}"  # type: ignore[no-any-return]

@wf.register(name="multiple_choice_message_many", description="Multiple choice - many")
def multiple_choice_many_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    answer = ui.multiple_choice(
        sender="Workflow",
        recipient="User",
        prompt="When was the last time you have run automated tests?",
        choices=["I am currently running them", "yesterday", "Tests? What tests??"],
        single=False
    )
    return f"you have chosen: {answer}"  # type: ignore[no-any-return]


@wf.register(name="suggested_function_call_message", description="Suggested Function Call Message")
def suggested_function_call_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    ui.suggested_function_call(
        sender="Workflow",
        recipient="User",
        function_name="the name of the function"
    )
    return "Completed OK"  # type: ignore[no-any-return]

@wf.register(name="function_call_execution_message", description="Function Call Execution Message")
def function_call_execution(
    ui: UI, params: dict[str, Any]
) -> str:
    ui.function_call_execution(
        sender="Workflow",
        recipient="User",
        function_name="the name of the function"
    )
    return "Completed OK"  # type: ignore[no-any-return]

@wf.register(name="error_message", description="Error Message")
def error_message(
    ui: UI, params: dict[str, Any]
) -> str:
    ui.error(
        sender="Workflow",
        recipient="User",
        short="This is an Error in short form",
        long="This is an Error in somewhat longer form"
    )
    return "Completed OK"  # type: ignore[no-any-return]

@wf.register(name="workflow_started", description="Workflow started")
def workflow_started(
    ui: UI, params: dict[str, Any]
) -> str:
    ui.workflow_started(
        sender="Workflow",
        recipient="User",
        name="_workflow_started_",
        description="The beginnings are delicate times...",
    )
    return "Completed OK"  # type: ignore[no-any-return]

@wf.register(name="workflow_completed", description="Workflow completed")
def workflow_completed(
    ui: UI, params: dict[str, Any]
) -> str:
    ui.workflow_completed(
        sender="Workflow",
        recipient="User",
        result="This workflow has completed",
    )
    return "Completed OK"  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=MesopUI(), title="Learning Chat")
