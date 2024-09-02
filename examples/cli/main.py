import logging
from typing import Annotated

from autogen import register_function
from autogen.agentchat import ConversableAgent
from fixtures import openai_gpt4o_mini_llm_config

from fastagency.core import Chatable, IOMessage
from fastagency.core.io.console import ConsoleIO
from fastagency.core.runtimes.autogen.base import AutoGenWorkflows

from fastagency import FastAgency

# Get the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a stream handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


wf = AutoGenWorkflows()

@wf.register(name="simple_learning", description="Student and teacher learning chat")
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

    return chat_result.summary

app = FastAgency(wf=wf, io=ConsoleIO())
