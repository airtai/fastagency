from typing import Any, Dict

import pytest
from autogen.agentchat import ConversableAgent

from fastagency.core import ChatMessage, Chatable, ConsoleIO
from fastagency.core.autogen import AutoGenWorkflows


@pytest.mark.openai
def test_simple(openai_gpt4o_mini_llm_config: Dict[str, Any]) -> None:
    wf = AutoGenWorkflows()

    @wf.register(
        name="simple_learning", description="Student and teacher learning chat"
    )
    def simple_workflow(io: Chatable, initial_message: str, session_id: str) -> str:
        student_agent = ConversableAgent(
            name="Student_Agent",
            system_message="You are a student willing to learn.",
            llm_config=openai_gpt4o_mini_llm_config,
        )
        teacher_agent = ConversableAgent(
            name="Teacher_Agent",
            system_message="You are a math teacher.",
            llm_config=openai_gpt4o_mini_llm_config,
        )

        chat_result = student_agent.initiate_chat(
            teacher_agent,
            message=initial_message,
            summary_method="reflection_with_llm",
            max_turns=5,
        )

        return chat_result.summary  # type: ignore[no-any-return]

    initial_message = "What is triangle inequality?"

    io = ConsoleIO()

    io.print(
        ChatMessage(
            sender="user",
            recepient="workflow",
            heading="Workflow BEGIN",
            body=f"Starting workflow with initial_message: {initial_message}",
        )
    )

    result = wf.run(
        name="simple_learning",
        session_id="session_id",
        io=io.create_subconversation(),
        initial_message=initial_message,
    )

    io.print(
        ChatMessage(
            sender="user",
            recepient="workflow",
            heading="Workflow END",
            body=f"Ending workflow with result: {result}",
        )
    )
