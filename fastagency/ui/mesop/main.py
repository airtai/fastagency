import time
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Optional

import mesop as me

from ...logging import get_logger
from .components.inputs import input_text
from .data_model import Conversation, State
from .message import consume_responses, message_box
from .send_prompt import send_prompt_to_autogen
from .styles import MesopHomePageStyles

if TYPE_CHECKING:
    from .base import MesopUI

__all__ = ["me"]

# Get the logger
logger = get_logger(__name__)


DEFAULT_SECURITY_POLICY = me.SecurityPolicy(
    allowed_iframe_parents=["https://fastagency.ai"]
)


def create_home_page(
    ui: "MesopUI",
    *,
    styles: Optional[MesopHomePageStyles] = None,
    security_policy: Optional[me.SecurityPolicy] = None,
) -> Callable[[], None]:
    mhp = MesopHomePage(ui, styles=styles, security_policy=security_policy)

    return mhp.build()


@dataclass
class MesopHomePageParams:
    # header_title: str = "FastAgency - Mesop"
    conv_starter_text: str = "Enter a prompt to chat with FastAgency team"


class MesopHomePage:
    def __init__(
        self,
        ui: "MesopUI",
        *,
        params: Optional[MesopHomePageParams] = None,
        styles: Optional[MesopHomePageStyles] = None,
        security_policy: Optional[me.SecurityPolicy] = None,
    ) -> None:
        self._ui = ui
        self._params = params or MesopHomePageParams()
        self._styles = styles or MesopHomePageStyles()
        self._security_policy = security_policy or DEFAULT_SECURITY_POLICY

    def build(self) -> Callable[[], None]:
        @me.page(  # type: ignore[misc]
            path="/",
            stylesheets=self._styles.stylesheets,
            security_policy=self._security_policy,
        )
        def home_page() -> None:
            self.home_page()

        return home_page  # type: ignore[no-any-return]

    def home_page(self) -> None:
        try:
            state = me.state(State)
            with me.box(style=self._styles.root):
                self.past_conversations_box()
                if state.in_conversation:
                    self.conversation_box()
                else:
                    self.conversation_starter_box()
        except Exception as e:
            logger.error(f"home_page(): Error rendering home page: {e}")
            me.text(text="Error: Something went wrong, please check logs for details.")

    def header(self) -> None:
        with me.box(
            style=self._styles.header,
        ):
            me.text(
                self._ui.app.title,
                style=self._styles.header_text,
            )

    def past_conversations_box(self) -> None:
        def conversation_display_title(full_name: str, max_length: int) -> str:
            if len(full_name) <= max_length:
                return full_name
            else:
                return full_name[: max_length - 3] + "..."

        def select_past_conversation(ev: me.ClickEvent) -> Iterator[None]:
            id = ev.key
            state = me.state(State)
            conversations_with_id = list(
                filter(lambda c: c.id == id, state.past_conversations)
            )
            conversation = conversations_with_id[0]
            state.conversation = conversation
            state.in_conversation = True
            yield
            time.sleep(1)
            yield
            me.scroll_into_view(key="conversationtop")
            yield

        def on_show_hide(ev: me.ClickEvent) -> None:
            state.hide_past = not state.hide_past

        def on_start_new_conversation(ev: me.ClickEvent) -> None:
            state.in_conversation = False
            state.prompt = ""

        state = me.state(State)
        style = (
            self._styles.past_chats_hide
            if state.hide_past
            else self._styles.past_chats_show
        )
        with me.box(style=style):
            with me.box(
                style=self._styles.past_chats_inner,
            ):
                with me.content_button(
                    on_click=on_show_hide, disabled=not state.past_conversations
                ):
                    me.icon("menu")
                with me.content_button(
                    on_click=on_start_new_conversation,
                    disabled=not state.conversation.completed,
                ):
                    me.icon("rate_review")
            if not state.hide_past:
                for conversation in state.past_conversations:
                    with me.box(
                        key=conversation.id,  # they are GUIDs so should not clash with anything other on the page
                        on_click=select_past_conversation,
                        style=self._styles.past_chats_conv,
                    ):
                        me.text(
                            text=conversation_display_title(conversation.title, 128)
                        )

    def conversation_starter_box(self) -> None:
        with me.box(style=self._styles.chat_starter):
            self.header()
            with me.box(
                style=self._styles.conv_starter,
            ):
                me.text(
                    self._params.conv_starter_text,
                    style=self._styles.conv_starter_text,
                )
                input_text(
                    self.send_prompt,
                    key="prompt",
                    disabled=False,
                    style=self._styles.message.text_input_inner,
                )

    def send_prompt(self, prompt: str) -> Iterator[None]:
        ui = self._ui
        wf = ui.app.wf

        name = wf.names[0]

        state = me.state(State)
        # me.navigate("/conversation")
        conversation = Conversation(
            title=prompt, completed=False, waiting_for_feedback=False
        )
        state.conversation = conversation
        state.in_conversation = True
        yield
        responses = send_prompt_to_autogen(prompt=prompt, wf=wf, name=name)
        yield from consume_responses(responses)

    def conversation_box(self) -> None:
        state = me.state(State)
        conversation = state.conversation
        with me.box(style=self._styles.chat_starter):
            self.header()
            messages = conversation.messages
            with me.box(
                style=self._styles.conv_list,
            ):
                me.box(
                    key="conversationtop",
                    style=self._styles.conv_top,
                )
                for message in messages:
                    message_box(
                        message, conversation.is_from_the_past, styles=self._styles
                    )
                if messages:
                    me.box(
                        key="end_of_messages",
                        style=self._styles.conv_top,
                    )
