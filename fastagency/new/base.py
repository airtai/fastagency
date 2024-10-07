from collections.abc import AsyncGenerator, AsyncIterator, Awaitable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol
from uuid import UUID

from pydantic import UUID4

from fastagency.base import IOMessage


class Conversation:
    def __init__(
        self,
        *,
        provider: "ProviderProtocol",
        id: Optional[UUID] = None,
        name: Optional[str] = None,
        parent: Optional["Conversation"] = None,
    ) -> None:
        """Initialize the conversation with the provider.

        Args:
            provider: The provider that is handling the conversation.
            id: The ID of the conversation. If not provided (default), a new UUID4 will be generated.
            name: The name of the conversation.
            parent: The parent conversation
        """
        self._provider = provider
        self._id = id if id else UUID4()
        self._name = name
        self._parent = parent
        self._subconversations: list["Conversation"] = []

    @property
    def name(self) -> "ProviderProtocol":
        return self._provider

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    def parent(self) -> Optional["Conversation"]:
        return self._parent

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def subconversations(self) -> list["Conversation"]:
        return self._subconversations

    @property
    def all_subconversations(self) -> list["Conversation"]:
        # recursive function to get all subconversations
        all_subs = [s.all_subconversations for s in self._subconversations]

        # flatten the list
        all_subs_flat = [item for sublist in all_subs for item in sublist]

        return self._subconversations + all_subs_flat

    async def create_subconversation(
        self,
        *,
        id: Optional[UUID] = None,
        name: Optional[str] = None,
    ) -> "Conversation":
        """Create a new subconversation.

        Args:
            id: The ID of the conversation. If not provided (default), a new UUID4 will be generated.
            name: The name of the conversation.
        """
        subconversation = Conversation(
            provider=self._provider, id=id, name=name, parent=self
        )
        await self._provider.create_subconversation(subconversation)
        self._subconversations.append(subconversation)

        return subconversation

    async def get_message(self, response: Optional[str]) -> IOMessage:
        return await self._provider.get_message(self, response)


class ClientProtocol(Protocol):
    async def start(
        self, lifespan: Callable[[], Awaitable[Any]]
    ) -> AsyncGenerator[None]: ...

    async def process_message(self, message: IOMessage) -> Optional[str]: ...


class FastAPIConversationClient:  # Client
    def __init__(
        self,
        provider: "ProviderProtocol",
        *args: Any,
        port: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the conversation with the provider."""
        self._provider = provider
        self._port = port
        self._args = args
        self._kwargs = kwargs

    @classmethod
    async def create(cls, provider: "ProviderProtocol") -> ClientProtocol:
        raise NotImplementedError

    @asynccontextmanager
    async def start(
        self, lifespan: Callable[[], Awaitable[Any]]
    ) -> AsyncIterator[None]:
        raise NotImplementedError
        yield

    async def process_message(self, message: IOMessage) -> Optional[str]:
        raise NotImplementedError

    class Provider:
        """Provider for the FastAPIConversationClient."""

        def __init__(self: "ProviderProtocol", url: str) -> None:
            """Initialize the provider with the URL.

            Args:
                url: The URL of the provider.

            """
            self._url = url

        @asynccontextmanager
        async def start(
            self, lifespan: Callable[[], Awaitable[Any]]
        ) -> AsyncIterator[None]:
            raise NotImplementedError
            yield

        async def get_workflows(self) -> "list[WorkflowInfo]":
            raise NotImplementedError

        async def start_conversation(
            self, workflow_name: Optional[str], message: Optional[str]
        ) -> Conversation:
            raise NotImplementedError

        async def create_subconversation(
            self, superconversation: Conversation
        ) -> Conversation:
            raise NotImplementedError

        async def get_conversation(self, conversation_id: UUID) -> Conversation:
            raise NotImplementedError

        async def get_message(
            self, conversation: Conversation, response: Optional[str]
        ) -> IOMessage:
            raise NotImplementedError


@dataclass
class WorkflowInfo:
    name: str
    description: str


class ProviderProtocol(Protocol):
    async def start(
        self, lifespan: Callable[[], Awaitable[Any]]
    ) -> AsyncGenerator[None]: ...

    async def get_workflows(self) -> list[WorkflowInfo]: ...

    async def start_conversation(
        self, workflow_name: Optional[str], message: Optional[str]
    ) -> Conversation: ...

    async def create_subconversation(
        self, superconversation: Conversation
    ) -> Conversation: ...

    async def get_conversation(self, conversation_id: UUID) -> Conversation: ...

    async def get_message(
        self, conversation: Conversation, response: Optional[str]
    ) -> IOMessage: ...


class NatsProvider:  # implements WorkflowProviderProtocol
    @asynccontextmanager
    async def start(
        self, lifespan: Callable[[], Awaitable[Any]]
    ) -> AsyncIterator[None]:
        raise NotImplementedError
        yield

    async def get_workflows(self) -> list[WorkflowInfo]:
        raise NotImplementedError

    async def start_conversation(
        self, workflow_name: Optional[str], message: Optional[str]
    ) -> Conversation:
        raise NotImplementedError

    async def get_conversation(self, conversation_id: UUID) -> Conversation:
        raise NotImplementedError
