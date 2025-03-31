from typing import Annotated, Any, Optional, Union

from autogen.agentchat import AssistantAgent as AutoGenAssistantAgent
from autogen.agentchat import ConversableAgent as AutoGenConversableAgent
from autogen.agentchat.chat import ChatResult
from autogen.agentchat.contrib.web_surfer import WebSurferAgent as AutoGenWebSurferAgent
from pydantic import BaseModel, Field, HttpUrl

__all__ = ["WebSurferAnswer", "WebSurferTool"]


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


class WebSurferTool:  # implements Toolable
    def __init__(
        self,
        *,
        name_prefix: str,
        llm_config: dict[str, Any],
        summarizer_llm_config: dict[str, Any],
        viewport_size: int = 4096,
        bing_api_key: Optional[str] = None,
        max_consecutive_auto_reply: int = 30,
        max_links_to_click: int = 10,
        websurfer_kwargs: Optional[dict[str, Any]] = None,
        assistant_kwargs: Optional[dict[str, Any]] = None,
    ):
        """Create a new WebSurferChat instance.

        Args:
            name_prefix (str): The name prefix of the inner AutoGen agents
            llm_config (Dict[str, Any]): The LLM configuration
            summarizer_llm_config (Dict[str, Any]): The summarizer LLM configuration
            viewport_size (int, optional): The viewport size. Defaults to 4096.
            bing_api_key (Optional[str], optional): The Bing API key. Defaults to None.
            max_consecutive_auto_reply (int, optional): The maximum consecutive auto reply. Defaults to 30.
            max_links_to_click (int, optional): The maximum links to click. Defaults to 10.
            websurfer_kwargs (Optional[Dict[str, Any]], optional): The WebSurfer kwargs. Defaults to None.
            assistant_kwargs (Optional[Dict[str, Any]], optional): The Assistant kwargs. Defaults to None.
        """
        if websurfer_kwargs is None:
            websurfer_kwargs = {}
        if assistant_kwargs is None:
            assistant_kwargs = {}

        self.name_prefix = name_prefix
        self.llm_config = llm_config
        self.summarizer_llm_config = summarizer_llm_config
        self.viewport_size = viewport_size
        self.bing_api_key = bing_api_key
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

    def create_new_task(
        self, task: Annotated[str, "a new task for websurfer to perform"]
    ) -> str:
        self.task = task
        try:
            answer = self._chat_with_websurfer(
                message=self.initial_message,
                clear_history=True,
            )
        except Exception as e:
            return self._get_error_from_exception(task, e)

        return self.create_final_reply(task, answer)

    def continue_task_with_additional_instructions(
        self, message: Annotated[str, "a followup message to the existing task"]
    ) -> str:
        try:
            answer = self._chat_with_websurfer(
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

    def register(
        self,
        *,
        caller: AutoGenConversableAgent,
        executor: Union[AutoGenConversableAgent, list[AutoGenConversableAgent]],
    ) -> None:
        @caller.register_for_llm(  # type: ignore[misc]
            name="create_new_websurfing_task",
            description="Creates a new task for a websurfer that can include searching or browsing the internet.",
        )
        def create_new_task(
            task: Annotated[str, "a new task for websurfer to perform"],
        ) -> str:
            return self.create_new_task(task)

        @caller.register_for_llm(  # type: ignore[misc]
            name="continue_websurfing_task_with_additional_instructions",
            description="Continue an existing task for a websurfer with additional instructions.",
        )
        def continue_task_with_additional_instructions(
            message: Annotated[
                str,
                "Additional instructions for the task after receiving the initial answer",
            ],
        ) -> str:
            return self.continue_task_with_additional_instructions(message)

        executors = executor if isinstance(executor, list) else [executor]
        for executor in executors:
            executor.register_for_execution(name="create_new_websurfing_task")(
                create_new_task
            )
            executor.register_for_execution(
                name="continue_websurfing_task_with_additional_instructions"
            )(continue_task_with_additional_instructions)
