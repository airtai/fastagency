from typing import Any, Optional, Union

from autogen import AssistantAgent, ConversableAgent

from ..tools import WebSurferTool


class WebSurferAgent(AssistantAgent):  # type: ignore[misc]
    def __init__(
        self,
        *args: Any,
        name: str,
        llm_config: dict[str, Any],
        summarizer_llm_config: dict[str, Any],
        executor: Union[ConversableAgent, list[ConversableAgent]],
        system_message: str = "You are a web surfer",
        bing_api_key: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize the WebSurferAgent.

        Args:
            *args (Any): The positional arguments.
            name (str): The name of the agent.
            llm_config (dict[str, Any]): The LLM configuration.
            summarizer_llm_config (dict[str, Any]): The summarizer LLM configuration.
            executor (Union[ConversableAgent, list[ConversableAgent]]): The executor agent(s).
            system_message (str): The system message.
            bing_api_key (Optional[str]): The Bing API key
            **kwargs (Any): The keyword arguments.
        """
        super().__init__(
            *args,
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            **kwargs,
        )
        self.web_surfer_tool = WebSurferTool(
            name_prefix="Web_Surfer",
            llm_config=llm_config,
            summarizer_llm_config=summarizer_llm_config,
            bing_api_key=bing_api_key,
        )
        self.web_surfer_tool.register(caller=self, executor=executor)
