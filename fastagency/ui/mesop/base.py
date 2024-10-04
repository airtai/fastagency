import threading
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from tempfile import TemporaryDirectory
from typing import Any, Callable, ClassVar, Optional
from uuid import uuid4

import mesop as me
from mesop.bin.bin import FLAGS as MESOP_FLAGS
from mesop.bin.bin import main as mesop_main

from ...base import (
    AskingMessage,
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    Runnable,
    TextInput,
    TextMessage,
    WorkflowCompleted,
    Workflows,
)
from ...logging import get_logger
from .styles import MesopHomePageStyles

logger = get_logger(__name__)


@dataclass
class MesopMessage:
    """A Mesop message."""

    io_message: IOMessage
    conversation: "MesopUI"


class MesopUI(IOMessageVisitor):  # UI
    _import_string: Optional[str] = None
    _main_path: Optional[str] = None
    _created_instance: Optional["MesopUI"] = None
    _app: Optional[Runnable] = None
    _me: Optional[Callable[..., Any]] = None

    def __init__(
        self,
        super_conversation: "Optional[MesopUI]" = None,
        *,
        security_policy: Optional[me.SecurityPolicy] = None,
        styles: Optional[MesopHomePageStyles] = None,
    ) -> None:
        """Initialize the console UI object.

        Args:
            super_conversation (Optional[MesopUI], optional): The super conversation. Defaults to None.
            security_policy (Optional[me.SecurityPolicy], optional): The security policy. Defaults to None.
            styles (Optional[MesopHomePageStyles], optional): The styles. Defaults to None.
        """
        logger.info(f"Initializing MesopUI: {self}")
        try:
            self.id: str = uuid4().hex
            self.super_conversation: Optional[MesopUI] = super_conversation
            self.sub_conversations: list[MesopUI] = []
            self._in_queue: Optional[Queue[str]] = None
            self._out_queue: Optional[Queue[MesopMessage]] = None

            if super_conversation is None:
                self._in_queue = Queue()
                self._out_queue = Queue()
            MesopUI.register(self)

            if MesopUI._me is None:
                from .main import create_home_page, me

                create_home_page(self, security_policy=security_policy, styles=styles)
                MesopUI._me = me

        except Exception as e:
            logger.error(e, exc_info=True)
            raise
        logger.info(f"Initialized MesopUI: {self}")

    _registry: ClassVar[dict[str, "MesopUI"]] = {}

    @classmethod
    def get_created_instance(cls) -> "MesopUI":
        created_instance = cls._created_instance
        if created_instance is None:
            raise RuntimeError("MesopUI has not been created yet.")

        return created_instance

    @property
    def app(self) -> Runnable:
        app = MesopUI._app
        if app is None:
            logger.error("MesopUI has not been created yet.")
            raise RuntimeError("MesopUI has not been created yet.")

        return app

    @contextmanager
    def create(self, app: Runnable, import_string: str) -> Iterator[None]:
        logger.info(f"Creating MesopUI with import string: {import_string}")
        MesopUI._app = app
        MesopUI._import_string = import_string

        start_script = """import fastagency.ui.mesop.main"""

        with TemporaryDirectory() as temp_dir:
            main_path = Path(temp_dir) / "main.py"
            with main_path.open("w") as f:
                f.write(start_script)

            MESOP_FLAGS.mark_as_parsed()
            MesopUI._main_path = str(main_path)
            MesopUI._created_instance = self

            yield

    def start(
        self,
        *,
        app: Runnable,
        import_string: str,
        name: Optional[str] = None,
        initial_message: Optional[str] = None,
        single_run: bool = False,
    ) -> None:
        logger.info(
            f"Starting MesopUI: import_string={self._import_string}, main_path={self._main_path}"
        )
        if single_run:
            logger.warning("single_run parameter is currently not supported in MesopUI")

        MesopUI._app = app

        mesop_main(["mesop", self._main_path])

    @classmethod
    def register(cls, conversation: "MesopUI") -> None:
        cls._registry[conversation.id] = conversation

    @classmethod
    def get_conversation(cls, id: str) -> "MesopUI":
        return cls._registry[id]

    @classmethod
    def unregister(cls, conversation: "MesopUI") -> None:
        del cls._registry[conversation.id]

    @property
    def is_root_conversation(self) -> bool:
        return self.super_conversation is not None

    @property
    def root_conversation(self) -> "MesopUI":
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

    def create_subconversation(self) -> "MesopUI":
        sub_conversation = MesopUI(self)
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

    def handle_wsgi(
        self,
        app: "Runnable",
        environ: dict[str, Any],
        start_response: Callable[..., Any],
    ) -> list[bytes]:
        logger.info(f"Starting MesopUI using WSGI interface with app: {app}")
        MesopUI._created_instance = self
        MesopUI._app = app

        if MesopUI._me is None:
            logger.error("MesopUI._me is None")
            raise RuntimeError("MesopUI._me is None")

        return MesopUI._me(environ, start_response)  # type: ignore[no-any-return]


def run_workflow(wf: Workflows, name: str, initial_message: str) -> MesopUI:
    def conversation_worker(ui: MesopUI, subconversation: MesopUI) -> None:
        ui.process_message(
            IOMessage.create(
                sender="user",
                recipient="workflow",
                type="system_message",
                message={
                    "heading": "Workflow BEGIN",
                    "body": f"Starting workflow with initial_message: {initial_message}",
                },
            )
        )

        try:
            result = wf.run(
                name=name,
                session_id="session_id",
                ui=subconversation,  # type: ignore[arg-type]
                initial_message=initial_message,
            )

            ui.process_message(
                IOMessage.create(
                    sender="user",
                    recipient="workflow",
                    type="system_message",
                    message={
                        "heading": "Workflow END",
                        "body": f"Ending workflow with result: {result}",
                    },
                )
            )

            ui.process_message(
                IOMessage.create(
                    sender="user",
                    recipient="workflow",
                    type="workflow_completed",
                    result=result,
                )
            )

        except Exception as ex:
            ui.process_message(
                IOMessage.create(
                    sender="system",
                    recipient="user",
                    type="error",
                    short=f"Exception raised: `{type(ex)}`",
                    long=str(ex.args[0]),
                )
            )

            ui.process_message(
                IOMessage.create(
                    sender="user",
                    recipient="workflow",
                    type="workflow_completed",
                    result="Exception raised",
                )
            )
            return

    ui = MesopUI()
    subconversation = ui.create_subconversation()
    thread = threading.Thread(target=conversation_worker, args=(ui, subconversation))
    thread.start()

    return subconversation

    # # needed for uvicorn to recognize the class as a valid ASGI application
    # async def __call__(
    #     self,
    #     scope: dict[str, Any],
    #     receive: Callable[[], Awaitable[dict]],
    #     send: Callable[[dict], Awaitable[None]],
    # ) -> None:
    #     MesopUI._created_instance = self
    #     from .main import me

    #     return await me(scope, receive, send)
