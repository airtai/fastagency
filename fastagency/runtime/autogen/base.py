import json
import os
import re
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Annotated, Any, Callable, Optional, Union

from asyncer import asyncify
from autogen.agentchat import AssistantAgent as AutoGenAssistantAgent
from autogen.agentchat import ConversableAgent
from autogen.agentchat.chat import ChatResult
from autogen.agentchat.contrib.web_surfer import WebSurferAgent as AutoGenWebSurferAgent
from autogen.io import IOStream
from pydantic import BaseModel, Field, HttpUrl

from ...base import (
    UI,
    AskingMessage,
    IOMessage,
    MessageType,
    MultipleChoice,
    TextInput,
    Workflow,
    Workflows,
)
from ...logging import get_logger

if TYPE_CHECKING:
    from fastagency.api.openapi import OpenAPI

__all__ = ["AutoGenWorkflows", "IOStreamAdapter", "WebSurferAnswer", "WebSurferChat"]


# Get the logger
logger = get_logger(__name__)

logger.info("Importing autogen.base.py")

_patterns = {
    "end_of_message": (
        "^\\n--------------------------------------------------------------------------------\\n$",
    ),
    "auto_reply": (
        "^\\x1b\\[31m\\n>>>>>>>> USING AUTO REPLY...\\x1b\\[0m\\n$",
        "^\\n>>>>>>>> USING AUTO REPLY...\\n$",
    ),
    "sender_recipient": (
        "^\\x1b\\[33m([a-zA-Z0-9_-]+)\\x1b\\[0m \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
        "^([a-zA-Z0-9_-]+) \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
    ),
    "suggested_function_call": (
        "^\\x1b\\[32m\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
        "^\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\n$",
    ),
    "stars": ("^\\x1b\\[32m(\\*{69}\\*+)\\x1b\\[0m\n$", "^(\\*{69}\\*+)\\n$"),
    "function_call_execution": (
        "^\\x1b\\[35m\\n>>>>>>>> EXECUTING FUNCTION ([a-zA-Z_]+)...\\x1b\\[0m\\n$",
        "^\\n>>>>>>>> EXECUTING FUNCTION ([a-zA-Z_]+)...\\n$",
    ),
    "response_from_calling_tool": (
        "^\\x1b\\[32m\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
        "^\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\n$",
    ),
    "no_human_input_received": (
        "^\\x1b\\[31m\\n>>>>>>>> NO HUMAN INPUT RECEIVED\\.\\x1b\\[0m$",
        "^\\n>>>>>>>> NO HUMAN INPUT RECEIVED\\.$",
    ),
    "user_interrupted": ("^USER INTERRUPTED\\n$",),
    "arguments": ("^Arguments: \\n(.*)\\n$",),
    "auto_reply_input": (
        "^Replying as ([a-zA-Z0-9_]+). Provide feedback to ([a-zA-Z0-9_]+). Press enter to skip and use auto-reply, or type 'exit' to end the conversation: $",
    ),
}


def _match(key: str, string: str, /) -> bool:
    return any(re.match(pattern, string) for pattern in _patterns[key])


def _findall(key: str, string: str, /) -> tuple[str, ...]:
    for pattern in _patterns[key]:
        if re.match(pattern, string):
            return re.findall(pattern, string)[0]  # type: ignore[no-any-return]
    return ()  # type: ignore[no-any-return]


@dataclass
class CurrentMessage:
    sender: Optional[str] = None
    recipient: Optional[str] = None
    type: MessageType = "text_message"
    auto_reply: bool = False
    body: Optional[str] = None
    call_id: Optional[str] = None
    function_name: Optional[str] = None
    arguments: Optional[dict[str, Any]] = None
    retval: Optional[Any] = None

    def process_chunk(self, chunk: str) -> bool:  # noqa: C901
        # logger.info(f"CurrentMessage.process_chunk({chunk=}):")
        if _match("end_of_message", chunk):
            return True

        if _match("auto_reply", chunk):
            # logger.info("CurrentMessage.process_chunk(): auto_reply detected")
            self.auto_reply = True
        elif _match("sender_recipient", chunk):
            # logger.info("CurrentMessage.process_chunk(): sender_recipient detected")
            self.sender, self.recipient = _findall("sender_recipient", chunk)
        elif _match("suggested_function_call", chunk):
            # logger.info("CurrentMessage.process_chunk(): suggested_function_call detected")
            self.call_id, self.function_name = _findall(
                "suggested_function_call", chunk
            )
            self.type = "suggested_function_call"
        elif _match("stars", chunk):
            # logger.info("CurrentMessage.process_chunk(): stars detected")
            pass
        elif _match("function_call_execution", chunk):
            # logger.info("CurrentMessage.process_chunk(): function_call_execution detected")
            self.function_name = _findall("function_call_execution", chunk)  # type: ignore[assignment]
            self.type = "function_call_execution"
        elif _match("response_from_calling_tool", chunk):
            # logger.info("CurrentMessage.process_chunk(): response_from_calling_tool detected")
            self.type = "function_call_execution"
            self.call_id = _findall("response_from_calling_tool", chunk)  # type: ignore[assignment]
        elif _match("no_human_input_received", chunk):
            # logger.info("CurrentMessage.process_chunk(): no_human_input_received detected")
            pass
        elif _match("user_interrupted", chunk):
            # logger.info("CurrentMessage.process_chunk(): user_interrupted detected")
            pass
        else:
            if self.type == "suggested_function_call":
                if _match("arguments", chunk):
                    # logger.info("CurrentMessage.process_chunk(): parsing arguments")
                    arguments_json: str = _findall("arguments", chunk)  # type: ignore[assignment]
                    self.arguments = json.loads(arguments_json)
                else:
                    logger.warning(
                        f"CurrentMessage.process_chunk(): unexpected chunk: {chunk=}, {self=}"
                    )
            elif self.type == "function_call_execution":
                # logger.info("CurrentMessage.process_chunk(): parsing retval")
                self.retval = chunk
            else:
                # logger.info("CurrentMessage.process_chunk(): parsing body")
                self.body = chunk if self.body is None else self.body + chunk

        return False

    def process_input(
        self, prompt: str, password: bool, messages: list[IOMessage]
    ) -> AskingMessage:
        last_message = messages[-1]
        sender, recipient = None, None
        message: AskingMessage

        if _match("auto_reply_input", prompt):
            # logger.info("IOStreamAdapter.input(): auto_reply_input detected")
            sender, recipient = _findall("auto_reply_input", prompt)  # type: ignore[assignment]

        if last_message.type == "suggested_function_call":
            # logger.info("IOStreamAdapter.input(): suggested_function_call detected")
            message = MultipleChoice(
                sender=sender,
                recipient=recipient,
                prompt="Please approve the suggested function call.",
                choices=["Approve", "Reject", "Exit"],
                default="Approve",
            )
        else:
            # logger.info("IOStreamAdapter.input(): text_message detected")
            message = TextInput(
                sender=None, recipient=None, prompt=prompt, password=password
            )

        return message

    def create_message(self) -> IOMessage:
        kwargs = {k: v for k, v in asdict(self).items() if v is not None}
        # logger.info(f"CurrentMessage.create_message(): {kwargs=}")
        return IOMessage.create(**kwargs)


class IOStreamAdapter:  # IOStream
    def __init__(self, ui: UI) -> None:
        """Initialize the adapter with a ChatableIO object.

        Args:
            ui (ChatableIO): The ChatableIO object to adapt

        """
        self.ui = ui
        self.current_message = CurrentMessage()

        self.messages: list[IOMessage] = []
        if not isinstance(self.ui, UI):
            raise ValueError("The ui object must be an instance of UI.")

    def _process_message_chunk(self, chunk: str) -> bool:
        if self.current_message.process_chunk(chunk):
            msg = self.current_message.create_message()
            self.messages.append(msg)
            self.current_message = CurrentMessage()

            return True
        else:
            return False

    def print(
        self, *objects: Any, sep: str = " ", end: str = "\n", flush: bool = False
    ) -> None:
        # logger.info(f"print(): {objects=}, {sep=}, {end=}, {flush=}")
        body = sep.join(map(str, objects)) + end
        ready_to_send = self._process_message_chunk(body)
        if ready_to_send:
            message = self.messages[-1]
            self.ui.process_message(message)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        # logger.info(f"input(): {prompt=}, {password=}")
        message: AskingMessage = self.current_message.process_input(
            prompt, password, self.messages
        )

        retval: str = self.ui.process_message(message)  # type: ignore[assignment]

        # in case of approving a suggested function call, we need to return an empty string to AutoGen
        if (
            message.type == "multiple_choice"
            and self.messages[-1].type == "suggested_function_call"
            and retval == "Approve"
        ):
            retval = ""
        if retval == "Exit":
            retval = "exit"

        # logger.info(f"input(): {retval=}")
        return retval


class AutoGenWorkflows(Workflows):
    def __init__(self) -> None:
        """Initialize the workflows."""
        self._workflows: dict[
            str, tuple[Callable[[Workflows, UI, str, str], str], str]
        ] = {}

    def register(
        self, name: str, description: str, *, fail_on_redefintion: bool = False
    ) -> Callable[[Workflow], Workflow]:
        def decorator(func: Workflow) -> Workflow:
            if name in self._workflows:
                if fail_on_redefintion:
                    raise ValueError(f"A workflow with name '{name}' already exists.")
                else:
                    logger.warning(f"Overwriting workflow with name '{name}'")

            self._workflows[name] = func, description
            return func

        return decorator

    def run(self, name: str, session_id: str, ui: UI, initial_message: str) -> str:
        workflow, description = self._workflows[name]

        iostream = IOStreamAdapter(ui)

        with IOStream.set_default(iostream):
            return workflow(self, ui, initial_message, session_id)

    @property
    def names(self) -> list[str]:
        return list(self._workflows.keys())

    def get_description(self, name: str) -> str:
        _, description = self._workflows.get(name, (None, "Description not available!"))
        return description

    def register_api(
        self,
        api: "OpenAPI",
        callers: Union[ConversableAgent, Iterable[ConversableAgent]],
        executors: Union[ConversableAgent, Iterable[ConversableAgent]],
        functions: Optional[
            Union[str, Iterable[Union[str, Mapping[str, Mapping[str, str]]]]]
        ] = None,
    ) -> None:
        if not isinstance(callers, Iterable):
            callers = [callers]
        if not isinstance(executors, Iterable):
            executors = [executors]
        if isinstance(functions, str):
            functions = [functions]

        for caller in callers:
            api._register_for_llm(caller, functions=functions)

        for executor in executors:
            api._register_for_execution(executor, functions=functions)


class WebSurferAnswer(BaseModel):
    task: Annotated[str, Field(..., description="The task to be completed")]
    is_successful: Annotated[
        bool, Field(..., description="Whether the task was successful")
    ]
    short_answer: Annotated[
        str,
        Field(
            ...,
            description="The short answer to the task without any explanation",
        ),
    ]
    long_answer: Annotated[
        str,
        Field(..., description="The long answer to the task with explanation"),
    ]
    visited_links: Annotated[
        list[HttpUrl],
        Field(..., description="The list of visited links to generate the answer"),
    ]

    @staticmethod
    def get_example_answer() -> "WebSurferAnswer":
        return WebSurferAnswer(
            task="What is the most popular QLED TV to buy on amazon.com?",
            is_successful=True,
            short_answer='Amazon Fire TV 55" Omni QLED Series 4K UHD smart TV',
            long_answer='Amazon has the best selling page by different categories and there is a category for QLED TVs under electroincs. The most popular QLED TV is Amazon Fire TV 55" Omni QLED Series 4K UHD smart TV, Dolby Vision IQ, Fire TV Ambient Experience, local dimming, hands-free with Alexa. It is the best selling QLED TV on Amazon.',
            visited_links=[
                "https://www.amazon.com/Best-Sellers/",
                "https://www.amazon.com/Best-Sellers-Electronics-QLED-TVs/",
            ],
        )


class WebSurferChat:
    def __init__(
        self,
        name_prefix: str,
        llm_config: dict[str, Any],
        summarizer_llm_config: dict[str, Any],
        viewport_size: int,
        bing_api_key: Optional[str],
        max_consecutive_auto_reply: int = 30,
        max_links_to_click: int = 10,
        websurfer_kwargs: dict[str, Any] = {},  # noqa: B006
        assistant_kwargs: dict[str, Any] = {},  # noqa: B006
    ):
        """Create a new WebSurferChat instance.

        Args:
            name_prefix (str): The name prefix of the inner AutoGen agents
            llm_config (Dict[str, Any]): The LLM configuration
            summarizer_llm_config (Dict[str, Any]): The summarizer LLM configuration
            viewport_size (int): The viewport size of the browser
            bing_api_key (Optional[str]): The Bing API key for the browser
            max_consecutive_auto_reply (int, optional): The maximum consecutive auto reply. Defaults to 30.
            max_links_to_click (int, optional): The maximum links to click. Defaults to 10.
            websurfer_kwargs (Dict[str, Any], optional): The keyword arguments for the websurfer. Defaults to {}.
            assistant_kwargs (Dict[str, Any], optional): The keyword arguments for the assistant. Defaults to {}.

        """
        self.name_prefix = name_prefix
        self.llm_config = llm_config
        self.summarizer_llm_config = summarizer_llm_config
        self.viewport_size = viewport_size
        self.bing_api_key = (
            bing_api_key if bing_api_key is not None else os.getenv("BING_API_KEY")
        )
        self.max_consecutive_auto_reply = max_consecutive_auto_reply
        self.max_links_to_click = max_links_to_click
        self.websurfer_kwargs = websurfer_kwargs
        self.assistant_kwargs = assistant_kwargs

        self.task = "not set yet"
        self.last_is_termination_msg_error = ""

        self.browser_config = {
            "viewport_size": self.viewport_size,
            "bing_api_key": self.bing_api_key,
            "request_kwargs": {
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
                }
            },
        }

        if "human_input_mode" in self.websurfer_kwargs:
            self.websurfer_kwargs.pop("human_input_mode")

        self.websurfer = AutoGenWebSurferAgent(
            name=f"{self.name_prefix}_inner_websurfer",
            llm_config=self.llm_config,
            summarizer_llm_config=self.summarizer_llm_config,
            browser_config=self.browser_config,
            human_input_mode="NEVER",
            is_termination_msg=self.is_termination_msg,
            **self.websurfer_kwargs,
        )

        if "human_input_mode" in self.assistant_kwargs:
            self.assistant_kwargs.pop("human_input_mode")

        self.assistant = AutoGenAssistantAgent(
            name=f"{self.name_prefix}_inner_assistant",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            system_message=self.system_message,
            max_consecutive_auto_reply=self.max_consecutive_auto_reply,
            # is_termination_msg=self.is_termination_msg,
            **self.assistant_kwargs,
        )

    def is_termination_msg(self, msg: dict[str, Any]) -> bool:
        # print(f"is_termination_msg({msg=})")
        if (
            "content" in msg
            and msg["content"] is not None
            and "TERMINATE" in msg["content"]
        ):
            return True
        try:
            WebSurferAnswer.model_validate_json(msg["content"])
            return True
        except Exception as e:
            self.last_is_termination_msg_error = str(e)
            return False

    def _get_error_message(self, chat_result: ChatResult) -> Optional[str]:
        messages = [msg["content"] for msg in chat_result.chat_history]
        last_message = messages[-1]
        if "TERMINATE" in last_message:
            return self.error_message

        try:
            WebSurferAnswer.model_validate_json(last_message)
        except Exception:
            return self.error_message

        return None

    def _get_answer(self, chat_result: ChatResult) -> WebSurferAnswer:
        messages = [msg["content"] for msg in chat_result.chat_history]
        last_message = messages[-1]
        return WebSurferAnswer.model_validate_json(last_message)

    def _chat_with_websurfer(
        self, message: str, clear_history: bool, **kwargs: Any
    ) -> WebSurferAnswer:
        msg: Optional[str] = message

        while msg is not None:
            chat_result = self.websurfer.initiate_chat(
                self.assistant,
                clear_history=clear_history,
                message=msg,
            )
            msg = self._get_error_message(chat_result)
            clear_history = False

        return self._get_answer(chat_result)

    def _get_error_from_exception(self, task: str, e: Exception) -> str:
        answer = WebSurferAnswer(
            task=task,
            is_successful=False,
            short_answer="unexpected error occurred",
            long_answer=str(e),
            visited_links=[],
        )

        return self.create_final_reply(task, answer)

    def create_final_reply(self, task: str, message: WebSurferAnswer) -> str:
        retval = (
            "We have successfully completed the task:\n\n"
            if message.is_successful
            else "We have failed to complete the task:\n\n"
        )
        retval += f"{task}\n\n"
        retval += f"Short answer: {message.short_answer}\n\n"
        retval += f"Explanation: {message.long_answer}\n\n"
        retval += "Visited links:\n"
        for link in message.visited_links:
            retval += f"  - {link}\n"

        return retval

    async def create_new_task(self, task: str) -> str:
        self.task = task
        try:
            answer = await asyncify(self._chat_with_websurfer)(
                message=self.initial_message,
                clear_history=True,
            )
        except Exception as e:
            return self._get_error_from_exception(task, e)

        return self.create_final_reply(task, answer)

    async def continue_task_with_additional_instructions(self, message: str) -> str:
        try:
            answer = await asyncify(self._chat_with_websurfer)(
                message=message,
                clear_history=False,
            )
        except Exception as e:
            return self._get_error_from_exception(message, e)

        return self.create_final_reply(message, answer)

    @property
    def example_answer(self) -> WebSurferAnswer:
        return WebSurferAnswer.get_example_answer()

    @property
    def initial_message(self) -> str:
        return f"""We are tasked with the following task:

{self.task}

If no link is provided in the task, you should search the internet first to find the relevant information.

The focus is on the provided url and its subpages, we do NOT care about the rest of the website i.e. parent pages.
e.g. If the url is 'https://www.example.com/products/air-conditioners', we are interested ONLY in the 'air-conditioners' and its subpages.

AFTER visiting the home page, create a step-by-step plan BEFORE visiting the other pages.
You can click on MAXIMUM {self.max_links_to_click} links. Do NOT try to click all the links on the page, but only the ones which are most relevant for the task (MAX {self.max_links_to_click})!
Do NOT visit the same page multiple times, but only once!
If your co-speaker repeats the same message, inform him that you have already answered to that message and ask him to proceed with the task.
e.g. "I have already answered to that message, please proceed with the task or you will be penalized!"
"""

    @property
    def error_message(self) -> str:
        return f"""Please output the JSON-encoded answer only in the following message before trying to terminate the chat.

IMPORTANT:
  - NEVER enclose JSON-encoded answer in any other text or formatting including '```json' ... '```' or similar!
  - NEVER write TERMINATE in the same message as the JSON-encoded answer!

EXAMPLE:

{self.example_answer.model_dump_json()}

NEGATIVE EXAMPLES:

1. Do NOT include 'TERMINATE' in the same message as the JSON-encoded answer!

{self.example_answer.model_dump_json()}

TERMINATE

2. Do NOT include triple backticks or similar!

```json
{self.example_answer.model_dump_json()}
```

THE LAST ERROR MESSAGE:

{self.last_is_termination_msg_error}

"""

    @property
    def system_message(self) -> str:
        return f"""You are in charge of navigating the web_surfer agent to scrape the web.
web_surfer is able to CLICK on links, SCROLL down, and scrape the content of the web page. e.g. you cen tell him: "Click the 'Getting Started' result".
Each time you receive a reply from web_surfer, you need to tell him what to do next. e.g. "Click the TV link" or "Scroll down".
It is very important that you explore ONLY the page links relevant for the task!

GUIDELINES:
- Once you retrieve the content from the received url, you can tell web_surfer to CLICK on links, SCROLL down...
By using these capabilities, you will be able to retrieve MUCH BETTER information from the web page than by just scraping the given URL!
You MUST use these capabilities when you receive a task for a specific category/product etc.
- do NOT try to create a summary without clicking on any link, because you will be missing a lot of information!
- if needed, you can instruct web surfer to SEARCH THE WEB for information.

Examples:
"Click the 'TVs' result" - This way you will navigate to the TVs section of the page and you will find more information about TVs.
"Click 'Electronics' link" - This way you will navigate to the Electronics section of the page and you will find more information about Electronics.
"Click the 'Next' button"
"Search the internet for the best TV to buy" - this will get links to initial pages to start the search

- Do NOT try to click all the links on the page, but only the ones which are RELEVANT for the task! Web pages can be very long and you will be penalized if spend too much time on this task!
- Your final goal is to summarize the findings for the given task. The summary must be in English!
- Create a summary after you successfully retrieve the information from the web page.
- It is useful to include in the summary relevant links where more information can be found.
e.g. If the page is offering to sell TVs, you can include a link to the TV section of the page.
- If you get some 40x error, please do NOT give up immediately, but try to navigate to another page and continue with the task.
Give up only if you get 40x error on ALL the pages which you tried to navigate to.


FINAL MESSAGE:
Once you have retrieved he wanted information, YOU MUST create JSON-encoded string. Summary created by the web_surfer is not enough!
You MUST not include any other text or formatting in the message, only JSON-encoded summary!

An example of the JSON-encoded summary:
{self.example_answer.model_dump_json()}

TERMINATION:
When YOU are finished and YOU have created JSON-encoded answer, write a single 'TERMINATE' to end the task.

OFTEN MISTAKES:
- Web surfer expects you to tell him what LINK NAME to click next, not the relative link. E.g. in case of '[Hardware](/Hardware), the proper command would be 'Click into 'Hardware''.
- Links presented are often RELATIVE links, so you need to ADD the DOMAIN to the link to make it work. E.g. link '/products/air-conditioners' should be 'https://www.example.com/products/air-conditioners'
- You do NOT need to click on MAX number of links. If you have enough information from the first xy links, you do NOT need to click on the rest of the links!
- Do NOT repeat the steps you have already completed!
- ALWAYS include the NEXT steps in the message!
- Do NOT instruct web_surfer to click on the same link multiple times. If there are some problems with the link, MOVE ON to the next one!
- Also, if web_surfer does not understand your message, just MOVE ON to the next link!
- NEVER REPEAT the same instructions to web_surfer! If he does not understand the first time, MOVE ON to the next link!
- NEVER enclose JSON-encoded answer in any other text or formatting including '```json' ... '```' or similar!
"""
