from typing import Any, Optional, Protocol, runtime_checkable

from fastagency.base import IOMessage


@runtime_checkable
class Conversable(Protocol):
    def init(
        self,
        provider: "Providable",
        id: str,
        *,
        name: Optional[str] = None,
        parent: Optional["Conversable"] = None,
    ) -> None: ...

    async def get_message(self) -> IOMessage: ...

    async def respond(self, response: str) -> None: ...

    def subconversations(self) -> list["Conversable"]: ...

    def all_sub_conversations(self) -> list["Conversable"]: ...


class FastAPIConversation:  # implements Conversable
    async def get_message(self) -> IOMessage:
        # get message from the user
        raise NotImplementedError

    async def respond(self, response: str) -> None:
        # respond to the user
        raise NotImplementedError

    def subconversations(self) -> list["Conversable"]:
        # return subconversations
        raise NotImplementedError

    def all_sub_conversations(self) -> list["Conversable"]:
        # return all subconversations
        raise NotImplementedError


class Providable(Protocol):
    async def get_workflows() -> list[dict[str, str]]: ...
    async def start_conversation(workflow_name: str, message: str) -> Conversable: ...


class FastAPIProvider:  # implements Providable
    async def get_workflows() -> list[dict[str, str]]:
        # get workflows
        raise NotImplementedError

    async def start_conversation(workflow_name: str, message: str) -> Conversable:
        # start conversation
        raise NotImplementedError

    def lifespan(self) -> callable[[...], Any]:
        # inspects the app, and figures out routes it needs
        raise NotImplementedError

    # additional methods to


class NatsProvider:  # implements Providable
    async def get_workflows() -> list[dict[str, str]]:
        # get workflows
        raise NotImplementedError

    async def start_conversation(workflow_name: str, message: str) -> Conversable:
        # start conversation
        raise NotImplementedError

    def lifespan(self) -> callable[[...], Any]:
        # inspects the app, and figures out routes it needs
        raise NotImplementedError

    # additional methods to
