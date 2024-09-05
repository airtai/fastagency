import threading
from dataclasses import dataclass
from queue import Queue
from typing import ClassVar, Dict, Generator, List, Optional
from uuid import uuid4

from fastagency.core.runtimes.autogen.base import AutoGenWorkflows

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

    io_message: IOMessage
    conversation: "MesopIO"


class MesopIO(IOMessageVisitor):
    def __init__(self, super_conversation: Optional["MesopIO"] = None) -> None:
        """Initialize the console IO object.

        Args:
            super_conversation (Optional[Chatable], optional): The super conversation. Defaults to None.
        """
        self.id: str = uuid4().hex
        self.super_conversation: Optional[MesopIO] = super_conversation
        self.sub_conversations: List[MesopIO] = []
        self._in_queue: Optional[Queue[str]] = None
        self._out_queue: Optional[Queue[MesopMessage]] = None
        if super_conversation is None:
            self._in_queue = Queue()
            self._out_queue = Queue()
        MesopIO.register(self)

    _registry: ClassVar[Dict[str, "MesopIO"]] = {}

    @classmethod
    def register(cls, conversation: "MesopIO") -> None:
        cls._registry[conversation.id] = conversation

    @classmethod
    def get_conversation(cls, id: str) -> "MesopIO":
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

    def _mesop_message(self, io_message: IOMessage) -> MesopMessage:
        return MesopMessage(
            conversation=self,
            io_message=io_message,
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
        cls, conversation_id: str, message: str
    ) -> Generator[MesopMessage, None, None]:
        conversation = cls.get_conversation(conversation_id)
        conversation.respond(message)
        return conversation.get_message_stream()

    def get_message_stream(self) -> Generator[MesopMessage, None, None]:
        while True:
            message = self.out_queue.get()
            if self._is_stream_braker(message.io_message):
                yield message
                break
            yield message


def run_workflow(wf: AutoGenWorkflows, name: str, initial_message: str) -> MesopIO:
    def conversation_worker(io: MesopIO, subconversation: MesopIO) -> None:
        io.process_message(
            IOMessage.create(
                sender="user",
                recepient="workflow",
                type="system_message",
                message={
                    "heading": "Workflow BEGIN",
                    "body": f"Starting workflow with initial_message: {initial_message}",
                },
            )
        )
        result = wf.run(
            name=name,
            session_id="session_id",
            io=subconversation,
            initial_message=initial_message,
        )
        io.process_message(
            IOMessage.create(
                sender="user",
                recepient="workflow",
                type="system_message",
                message={
                    "heading": "Workflow END",
                    "body": f"Ending workflow with result: {result}",
                },
            )
        )

        io.process_message(
            IOMessage.create(
                sender="user",
                recepient="workflow",
                type="workflow_completed",
                result=result,
            )
        )

    io = MesopIO()
    subconversation = io.create_subconversation()
    thread = threading.Thread(target=conversation_worker, args=(io, subconversation))
    thread.start()

    return subconversation
