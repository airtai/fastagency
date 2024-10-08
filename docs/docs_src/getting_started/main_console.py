import os
from typing import Any, Optional
from uuid import UUID

from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency, WorkflowsProtocol
from fastagency.runtimes.autogen import AutoGenWorkflows
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


@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(
    ui: UI, workflow_uuid: UUID, **kwargs: Any
) -> str:
    initial_message = ui.text_input(
        prompt="What do you want to learn about today?",
        workflow_uuid=workflow_uuid,
        sender="Workflow",
        recipient="User",
    )

    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
        llm_config=llm_config,
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
        llm_config=llm_config,
    )

    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI(), title="Learning Chat")
