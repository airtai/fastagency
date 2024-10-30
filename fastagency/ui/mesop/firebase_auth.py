import typing
from dataclasses import dataclass
from typing import Literal

import mesop as me

from .data_model import State

if typing.TYPE_CHECKING:
    from .auth import AuthProtocol


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

    # maybe me.Component is wrong
    def login_component(self) -> me.component:
        with me.box():
            state = me.state(State)

            me.text(f"state.authenticated_user: {state.authenticated_user or 'N/A' }")

    # maybe me.Component is wrong
    def logout_component(self) -> me.component:
        raise NotImplementedError
