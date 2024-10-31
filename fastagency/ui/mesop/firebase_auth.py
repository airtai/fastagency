import typing
from dataclasses import dataclass
from typing import Literal

import firebase_admin
import mesop as me
import mesop.labs as mel
from firebase_admin import auth

from .data_model import State
from .firebase_auth_component import firebase_auth_component
from .styles import MesopHomePageStyles

if typing.TYPE_CHECKING:
    from .auth import AuthProtocol


# Avoid re-initializing firebase app (useful for avoiding warning message because of hot reloads).
if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
    default_app = firebase_admin.initialize_app()


@dataclass
class FirebaseConfig:
    api_key: str
    auth_domain: str
    project_id: str
    storage_bucket: str
    messaging_sender_id: str
    app_id: str


class FirebaseAuth:  # implements AuthProtocol
    def __init__(
        self,
        sign_in_methods: set[Literal["google"]],
        config: FirebaseConfig,
    ) -> None:
        """Initialize the Firebase Auth provider.

        Args:
            sign_in_methods (set[Literal["google"]]): The sign-in methods to enable.
            config (FirebaseConfig): The Firebase configuration.
        """
        # mypy check if self is AuthProtocol
        _self: AuthProtocol = self

        if not sign_in_methods:
            raise ValueError("At least one sign-in method must be specified")

        self.sign_in_methods = sign_in_methods
        self.config = config

    def create_security_policy(self, policy: me.SecurityPolicy) -> me.SecurityPolicy:
        return me.SecurityPolicy(
            dangerously_disable_trusted_types=True,
            allowed_connect_srcs=list(
                set(policy.allowed_connect_srcs or []) | {"*.googleapis.com"}
            ),
            allowed_script_srcs=list(
                set(policy.allowed_script_srcs or [])
                | {
                    "*.google.com",
                    "https://www.gstatic.com",
                    "https://cdn.jsdelivr.net",
                }
            ),
        )

    @classmethod
    def on_auth_changed(cls, e: mel.WebEvent) -> None:
        firebase_auth_token = e.value
        if not firebase_auth_token:
            me.state(State).authenticated_user = ""
            return

        decoded_token = auth.verify_id_token(firebase_auth_token)
        # You can do an allowlist if needed.
        # if decoded_token["email"] != "allowlisted.user@gmail.com":
        #   raise me.MesopUserException("Invalid user: " + decoded_token["email"])
        me.state(State).authenticated_user = decoded_token["email"]

    # maybe me.Component is wrong
    def auth_component(self) -> me.component:
        styles = MesopHomePageStyles()
        state = me.state(State)
        if state.authenticated_user:
            firebase_auth_component(on_auth_changed=FirebaseAuth.on_auth_changed)
        else:
            with me.box(style=styles.login_box):  # noqa: SIM117
                with me.box(style=styles.login_btn_container):
                    me.text("Sign in to your account", style=styles.header_text)
                    firebase_auth_component(
                        on_auth_changed=FirebaseAuth.on_auth_changed
                    )
