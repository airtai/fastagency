import os
import typing
from typing import Any, Literal

import firebase_admin
import mesop as me
import mesop.labs as mel
from firebase_admin import auth

from .data_model import State
from .firebase_auth_component import FirebaseConfig, firebase_auth_component
from .styles import MesopHomePageStyles

__all__ = ["FirebaseConfig"]

if typing.TYPE_CHECKING:
    from .auth import AuthProtocol


# Avoid re-initializing firebase app (useful for avoiding warning message because of hot reloads).
if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
    default_app = firebase_admin.initialize_app()


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

        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise ValueError(
                "Error: A service account key is required. Please create one and set the JSON key file path in the `GOOGLE_APPLICATION_CREDENTIALS` environment variable. For more information: https://firebase.google.com/docs/admin/setup#initialize_the_sdk_in_non-google_environments"
            )

        if not os.getenv("AUTHORIZED_USER_EMAILS"):
            raise ValueError(
                """Error: The `AUTHORIZED_USER_EMAILS` environment variable is not set. This variable is required to control access to the application.

You can set it as:
- A comma-separated list of authorized email addresses, e.g., AUTHORIZED_USER_EMAILS=me@example.com,you@example.com,them@example.com
- Or, you can set it to "OPEN_ACCESS" to allow unrestricted access to all users.
"""
            )

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

    def is_authorized(self, token: dict[str, Any]) -> bool:
        """Check if the email in the token is authorized.

        The authorized emails are specified in the AUTHORIZED_USER_EMAILS environment variable. This variable should be a comma-separated list of email addresses or "OPEN_ACCESS". If the value is set to `OPEN_ACCESS`, it grants unrestricted access to anyone, regardless of their email address.

        Args:
            token (dict[str, Any]): The token to check, which must contain an 'email' key.

        Returns:
            bool: True if the email in the token is authorized, False otherwise.
        """
        # Retrieve the authorized emails from the environment variable and strip whitespace
        authorized_emails = os.getenv("AUTHORIZED_USER_EMAILS", "").split(",")

        # Check for open access
        if authorized_emails == ["OPEN_ACCESS"]:
            return True

        # Check if the email in the token is among the authorized emails
        return token.get("email") in [email.strip() for email in authorized_emails]

    def on_auth_changed(self, e: mel.WebEvent) -> None:
        state = me.state(State)
        firebase_auth_token = e.value

        if not firebase_auth_token:
            state.authenticated_user = ""
            return

        decoded_token = auth.verify_id_token(firebase_auth_token)

        if not self.is_authorized(decoded_token):
            raise me.MesopUserException(
                "You are not authorized to access this application. "
                "Please contact the application administrators for access."
            )

        state.authenticated_user = decoded_token["email"]

    # maybe me.Component is wrong
    def auth_component(self) -> me.component:
        styles = MesopHomePageStyles()
        state = me.state(State)
        if state.authenticated_user:
            with me.box(style=styles.logout_btn_container):
                firebase_auth_component(
                    on_auth_changed=self.on_auth_changed, config=self.config
                )
        else:
            with me.box(style=styles.login_box):  # noqa: SIM117
                with me.box(style=styles.login_btn_container):
                    me.text("Sign in to your account", style=styles.header_text)
                    firebase_auth_component(
                        on_auth_changed=self.on_auth_changed, config=self.config
                    )
