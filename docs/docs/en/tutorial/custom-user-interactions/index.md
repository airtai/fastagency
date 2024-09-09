# Custom User Interactions

In this example, we'll demonstrate how to create custom interaction with the user using [`Chatable`](../api/fastagency/core/Chatable.md) protocol and its [`process_message`](../api/fastagency/core/Chatable.md#fastagency.core.Chatable.create_subconversation) method.


## Install

To get started, you need to install FastAgency. You can do this using `pip`, Python's package installer.

```console
pip install "fastagency[autogen]"
```


## Define Interaction

This section describes how to define functions for the `ConversableAgent` instances representing the student and teacher. We will also explain the differences between `MultipleChoice`, `SystemMessage`, and `TextInput`, which are used for communication between the user and agents.

Let's define three functions which will be avaliable to the agents:

### Free Textual Tnput

`TextInput` is suitable for free-form text messages, ideal for open-ended queries and dialogues. This function allows the student to request exam questions from the teacher and provides some suggestions using `TextInput`.

```python
def retrieve_exam_questions(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = TextInput(
            sender="student",
            recepient="teacher",
            prompt=message,
            suggestions=["1) Mona Lisa", "2) Innovations", "3) Florence at the time of Leonardo", "4) The Last Supper", "5) Vitruvian Man"],
        )
        return io.process_message(msg)
    except Exception as e:
        return f"retrieve_exam_questions() FAILED! {e}"
```

### System Info Messages

`SystemMessage` is used for operational or system-related instructions, such as logging data, and is not part of the agent dialogue. This function logs the final answers after the student completes the discussion using `SystemMessage` to log the event.

```python
def write_final_answers(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = SystemMessage(
            sender="function call logger",
            recepient="system",
            message={
                "operation": "storing final answers",
                "content": message,
            },
        )
        io.process_message(msg)
        return "Final answers stored."
    except Exception as e:
        return f"write_final_answers() FAILED! {e}"
```

### Multiple Choice

`MultipleChoice` is used for structured responses where the user must select one of several predefined options. This function retrieves the final grade for the student's submitted answers using `MultipleChoice`, presenting the user with grading options.

```python
def get_final_grade(message: Annotated[str, "Message for examiner"]) -> str:
    try:
        msg = MultipleChoice(
            sender="student",
            recepient="teacher",
            prompt=message,
            choices=["A", "B", "C", "D", "F"],
        )
        return io.process_message(msg)
    except Exception as e:
        return f"get_final_grade() FAILED! {e}"
```

### Other Types of Messages

All supported messages are subclasses of the [IOMessage](../api/fastagency/core/IOMessage.md) base class.

## Registering the Functions
We now register these functions with the workflow, linking the `student_agent` as the caller and the `teacher_agent` as the executor.

```python
register_function(
    retrieve_exam_questions,
    caller=student_agent,
    executor=teacher_agent,
    name="retrieve_exam_questions",
    description="Get exam questions from examiner",
)

register_function(
    write_final_answers,
    caller=student_agent,
    executor=teacher_agent,
    name="write_final_answers",
    description="Write final answers to exam questions.",
)

register_function(
    get_final_grade,
    caller=student_agent,
    executor=teacher_agent,
    name="get_final_grade",
    description="Get the final grade after submitting answers.",
)
```

## Define FastAgency Application
Finally, we'll define the entire application:

```python
import os
from typing import Annotated

from autogen.agentchat import ConversableAgent
from autogen import register_function

from fastagency.core import Chatable
from fastagency.core.runtimes.autogen.base import AutoGenWorkflows

from fastagency.core.base import MultipleChoice, SystemMessage, TextInput

from fastagency import FastAgency


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


@wf.register(name="exam_practice", description="Student and teacher chat")
def exam_learning(io: Chatable, initial_message: str, session_id: str) -> str:

    def is_termination_msg(msg: str) -> bool:
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

    def retrieve_exam_questions(message: Annotated[str, "Message for examiner"]) -> str:
        try:
            msg = TextInput(
                sender="student",
                recepient="teacher",
                prompt=message,
                suggestions=["1) Mona Lisa", "2) Innovations", "3) Florence at the time of Leonardo", "4) The Last Supper", "5) Vitruvian Man"],
            )
            return io.process_message(msg)
        except Exception as e:
            return f"retrieve_exam_questions() FAILED! {e}"

    def write_final_answers(message: Annotated[str, "Message for examiner"]) -> str:
        try:
            msg = SystemMessage(
                sender="function call logger",
                recepient="system",
                message={
                    "operation": "storing final answers",
                    "content": message,
                },
            )
            io.process_message(msg)
            return "Final answers stored."
        except Exception as e:
            return f"write_final_answers() FAILED! {e}"

    def get_final_grade(message: Annotated[str, "Message for examiner"]) -> str:
        try:
            msg = MultipleChoice(
                    sender="student",
                    recepient="teacher",
                    prompt=message,
                    choices=["A", "B", "C", "D", "F"],
            )
            return io.process_message(msg)
        except Exception as e:
            return f"get_final_grade() FAILED! {e}"

    register_function(
        retrieve_exam_questions,
        caller=student_agent,
        executor=teacher_agent,
        name="retrieve_exam_questions",
        description="Get exam questions from examiner",
    )

    register_function(
        write_final_answers,
        caller=student_agent,
        executor=teacher_agent,
        name="write_final_answers",
        description="Write a final answers to exam questions to examiner, but only after discussing with the tutor first.",
    )

    register_function(
        get_final_grade,
        caller=student_agent,
        executor=teacher_agent,
        name="get_final_grade",
        description="Get the final grade after submitting the answers.",
    )

    chat_result = teacher_agent.initiate_chat(
        student_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary


from fastagency.core.io.console import ConsoleIO

app = FastAgency(wf=wf, io=ConsoleIO())
```

## Run Application

Once everything is set up, you can run your FastAgency application using the following command:

```console
fastagency run
```
