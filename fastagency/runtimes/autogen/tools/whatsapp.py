from typing import Union

from autogen import ConversableAgent

from fastagency.runtimes.autogen.autogen import Toolable


class WhatsAppTool(Toolable):
    def register(
        self,
        *,
        caller: ConversableAgent,
        executor: Union[ConversableAgent, list[ConversableAgent]],
    ) -> None:
        pass
