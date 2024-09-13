import os
from typing import Annotated, Any, Dict, Optional

from autogen import register_function
from autogen.agentchat import ConversableAgent

from fastagency import FastAgency
from fastagency import UI
from fastagency.base import MultipleChoice, SystemMessage, TextInput
from fastagency.ui.console import ConsoleUI
from fastagency.runtime.autogen.base import AutoGenWorkflows

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


@wf.register(name="exam_practice", description="Student and teacher chat")
def exam_learning(wf: AutoGenWorkflows, ui: UI, initial_message: str, session_id: str) -> Optional[str]:

    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student writing a practice test. Your task is as follows:\n"
        "  1) Retrieve exam questions by calling a function.\n"
        "  2) Write a draft of proposed answers and engage in dialogue with your tutor.\n"
        "  3) Once you are done with the dialogue, register the final answers by calling a function.\n"
        "  4) Retrieve the final grade by calling a function.\n"
        "Finally, terminate the chat by saying 'TERMINATE'.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a teacher.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # we can define several types of interactions with the UI
    wf.register_text_input(
        ui=ui,
        name="retrieve_exam_questions",
        description="Get exam questions from examiner",
        callers=student_agent,
        executors=teacher_agent,
        suggestions=[
            "1) Mona Lisa",
            "2) Innovations",
            "3) Florence at the time of Leonardo",
            "4) The Last Supper",
            "5) Vitruvian Man",
        ],
    )

    wf.register_system_message(
        ui=ui,
        name="write_final_answers",
        description="Write a final answers to exam questions to examiner, but only after discussing with the tutor first. ",
            # "Message sent should be in the format: {'operation': 'storing_final_answers', 'answers': 'insert your answers here'}.",
        callers=student_agent,
        executors=teacher_agent,
    )

    # wf.register_multiple_choice(
    #     ui=ui,
    #     name="get_final_grade",
    #     description="Get the final grade after submitting the answers.",
    #     callers=student_agent,
    #     executors=teacher_agent,
    #     choices=["A", "B", "C", "D", "F"],
    # )

    chat_result = teacher_agent.initiate_chat(
        student_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(wf=wf, ui=ConsoleUI())
