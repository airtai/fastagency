from typing import Any, Union

from autogen import AssistantAgent, ConversableAgent, LLMConfig

from ..tools import WhatsAppTool

WHATSAPP_SYSTEM_MESSAGE = """You are an agent in charge of communication with the WhatsAPP API.

When sending the message, the Body must use the following format:

{{
    "from": "{sender}",
    "to": "receiverNumber",
    "messageId": "test-message-randomInt",
    "content": {{
        "text": "message"
    }},
    "callbackData": "Callback data"
}}

"from" number is always the same.
"""


class WhatsAppAgent(AssistantAgent):  # type: ignore[misc]
    def __init__(
        self,
        *args: Any,
        name: str,
        llm_config: LLMConfig,
        executor: Union[ConversableAgent, list[ConversableAgent]],
        sender: str,
        whatsapp_api_key: str,
        **kwargs: Any,
    ):
        """Initialize the WhatsAppAgent.

        Args:
            *args (Any): The positional arguments.
            name (str): The name of the agent.
            llm_config (dict[str, Any]): The LLM configuration.
            executor (Union[ConversableAgent, list[ConversableAgent]]): The executor agent(s).
            sender (str): Number of the sender for WhatsApp API.
            whatsapp_api_key (str): The WhatsApp API key
            **kwargs (Any): The keyword arguments.
        """
        super().__init__(
            *args,
            name=name,
            system_message=WHATSAPP_SYSTEM_MESSAGE.format(sender=sender),
            llm_config=llm_config,
            **kwargs,
        )
        self.whatsapp_tool = WhatsAppTool(
            whatsapp_api_key=whatsapp_api_key,
        )

        self.whatsapp_tool.register(caller=self, executor=executor)
