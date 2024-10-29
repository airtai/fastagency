import os
from typing import Any

from autogen import ConversableAgent
from board import register_chess_functions

from fastagency import UI
from fastagency.logging import get_logger
from fastagency.runtimes.autogen import AutoGenWorkflows

logger = get_logger(__name__)

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

wf = AutoGenWorkflows()


@wf.register(name="chess", description="Chess playing between student and teacher")
def chess_workflow(ui: UI, params: dict[str, Any]) -> str:
    try:
        initial_message = (
            "This is a chat between Bobby Fischer and a young chess prodigy. "
            "Bobby Fischer will pick a board situation with maximum of 10 pieces on the board "
            "and give a task to its student such as checkmate to solve in a maximum of 3 turns. "
            "They will discuss potential moves and the strategy. "
            "When anlysis is performed, the student will write at potential reasonable resopnses to it moves. "
            "The student will play its move after the discussin and Bobby Fisher will play the other side."
        )

        student_agent = ConversableAgent(
            name="Alice",
            system_message="You are a child prodigy learning to play chess from Bobby Fischer.",
            llm_config=llm_config,
            # human_input_mode="ALWAYS",
        )
        teacher_agent = ConversableAgent(
            name="Bobby",
            system_message="You are Bobby Fischer teaching a young prodigy how to play.",
            llm_config=llm_config,
            # human_input_mode="ALWAYS",
        )

        register_chess_functions(student_agent, teacher_agent)

        chat_result = student_agent.initiate_chat(
            teacher_agent,
            message=initial_message,
            summary_method="reflection_with_llm",
            max_turns=40,
        )

        return chat_result.summary  # type: ignore[no-any-return]

    except Exception as e:
        logger.error(f"Error in chess_workflow: {e}", exc_info=True)
        raise
