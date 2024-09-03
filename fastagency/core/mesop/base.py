from dataclasses import dataclass
from queue import Queue
from typing import ClassVar, Dict, Generator, List, Optional
from uuid import UUID, uuid4

from ..base import (
    AskingMessage,
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    TextInput,
    TextMessage,
    WorkflowCompleted,
)


@dataclass
class MesopMessage:
    """A Mesop message."""

    message: IOMessage
    conversation: "MesopIO"


class MesopIO(IOMessageVisitor):
    def __init__(self, super_conversation: Optional["MesopIO"] = None) -> None:
        """Initialize the console IO object.

        Args:
            super_conversation (Optional[Chatable], optional): The super conversation. Defaults to None.
        """
        self.id: UUID = uuid4()
        self.super_conversation: Optional[MesopIO] = super_conversation
        self.sub_conversations: List[MesopIO] = []
        self._in_queue: Optional[Queue[str]] = None
        self._out_queue: Optional[Queue[MesopMessage]] = None
        if super_conversation is None:
            self._in_queue = Queue()
            self._out_queue = Queue()

    _registry: ClassVar[Dict[UUID, "MesopIO"]] = {}

    @classmethod
    def register(cls, conversation: "MesopIO") -> None:
        cls._registry[conversation.id] = conversation

    @classmethod
    def get_conversation(cls, id: UUID) -> "MesopIO":
        return cls._registry[id]

    @classmethod
    def unregister(cls, conversation: "MesopIO") -> None:
        del cls._registry[conversation.id]

    @property
    def is_root_conversation(self) -> bool:
        return self.super_conversation is not None

    @property
    def root_conversation(self) -> "MesopIO":
        if self.super_conversation is None:
            return self
        else:
            return self.super_conversation.root_conversation

    @property
    def in_queue(self) -> Queue[str]:
        queue = self.root_conversation._in_queue
        return queue  # type: ignore[return-value]

    @property
    def out_queue(self) -> Queue[MesopMessage]:
        queue = self.root_conversation._out_queue
        return queue  # type: ignore[return-value]

    @property
    def level(self) -> int:
        return (
            0 if self.super_conversation is None else self.super_conversation.level + 1
        )

    def _publish(self, mesop_msg: MesopMessage) -> None:
        self.out_queue.put(mesop_msg)

    def _mesop_message(self, mesop_msg: IOMessage) -> MesopMessage:
        return MesopMessage(
            conversation=self,
            message=mesop_msg,
        )

    def visit_default(self, message: IOMessage) -> None:
        mesop_msg = self._mesop_message(message)
        self._publish(mesop_msg)

    def visit_text_message(self, message: TextMessage) -> None:
        mesop_msg = self._mesop_message(message)
        self._publish(mesop_msg)

    def visit_text_input(self, message: TextInput) -> str:
        mesop_msg = self._mesop_message(message)
        self._publish(mesop_msg)
        return self.in_queue.get()

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        mesop_msg = self._mesop_message(message)
        self._publish(mesop_msg)
        return self.in_queue.get()

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)

    def create_subconversation(self) -> "MesopIO":
        sub_conversation = MesopIO(self)
        self.sub_conversations.append(sub_conversation)

        return sub_conversation

    def _is_stream_braker(self, message: IOMessage) -> bool:
        return isinstance(message, (AskingMessage, WorkflowCompleted))

    def respond(self, message: str) -> None:
        self.in_queue.put(message)

    @classmethod
    def respond_to(
        cls, conversation_id: UUID, message: str
    ) -> Generator[MesopMessage, None, None]:
        conversation = cls.get_conversation(conversation_id)
        conversation.respond(message)
        return conversation.get_chat_stream()

    def get_chat_stream(self) -> Generator[MesopMessage, None, None]:
        while True:
            message = self.out_queue.get()
            if self._is_stream_braker(message.message):
                yield message
                break
