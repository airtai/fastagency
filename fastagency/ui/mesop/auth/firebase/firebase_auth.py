import os
import typing
from typing import Any, Callable, Literal, Union

import firebase_admin
import mesop as me
import mesop.labs as mel
from firebase_admin import auth

from ...data_model import State
from ...styles import MesopHomePageStyles
from .firebase_auth_component import FirebaseConfig, firebase_auth_component

__all__ = ["FirebaseConfig"]

if typing.TYPE_CHECKING:
    from ..auth import AuthProtocol


# Avoid re-initializing firebase app (useful for avoiding warning message because of hot reloads).
if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
    default_app = firebase_admin.initialize_app()


class FirebaseAuth:  # implements AuthProtocol
    def __init__(
        self,
        sign_in_methods: list[Literal["google"]],
        config: FirebaseConfig,
        allowed_users: Union[
            list[str], Callable[[dict[str, Any]], bool], Literal["all"]
        ],  # for callable -> pass the whole decoded token (dict)
    ) -> None:
        """Initialize the Firebase Auth provider.

        Args:
            sign_in_methods: List of authentication methods to enable.
                Currently only supports ["google"].
            config: Firebase configuration containing project settings.
            allowed_users: Specifies user access control:
                - List[str]: List of allowed email addresses
                - Callable: Function taking decoded token and returning boolean
                - "all": Allows all authenticated users (default)

        Raises:
            TypeError: If sign_in_methods is not a list
            ValueError: If no sign-in methods specified, unsupported methods provided,
                or GOOGLE_APPLICATION_CREDENTIALS environment variable is missing
        """
        # mypy check if self is AuthProtocol
        _self: AuthProtocol = self

        self.config = config
        self.allowed_users = allowed_users

        # Validate sign_in_methods type
        if not isinstance(sign_in_methods, list):
            raise TypeError(
                "sign_in_methods must be a list. Example: sign_in_methods=['google']"
            )

        # 2. Remove duplicates
        self.sign_in_methods = list(set(sign_in_methods))

        # 3. Validate sign-in methods
        if not self.sign_in_methods:
            raise ValueError("At least one sign-in method must be specified")

        unsupported_methods = [
            method for method in self.sign_in_methods if method != "google"
        ]
        if unsupported_methods:
            raise ValueError(
                f"Unsupported sign-in method(s): {unsupported_methods}. Currently, only 'google' sign-in is supported."
            )

        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise ValueError(
                "Error: A service account key is required. Please create one and set the JSON key file path in the `GOOGLE_APPLICATION_CREDENTIALS` environment variable. For more information: https://firebase.google.com/docs/admin/setup#initialize_the_sdk_in_non-google_environments"
            )

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
        """Check if the user is authorized based on the token and allowed_users configuration.

        Args:
            token: The decoded Firebase JWT token containing user information.
                Must include an 'email' field for validation.

        Returns:
            bool: True if the user is authorized, False otherwise.

        Raises:
            TypeError: If allowed_users is not of type str, list, or Callable.
            ValueError: If email field is missing in the Firebase token.
        """
        # Check if the email is present in token
        email = token.get("email")
        if not email:
            raise ValueError(
                "Invalid response from Firebase: "
                "`email` field is missing in the token"
            )

        # Handle string-based configuration ("all" or single email)
        if isinstance(self.allowed_users, str):
            if self.allowed_users == "all":
                return True
            return email == self.allowed_users

        # Handle list of allowed email addresses
        if isinstance(self.allowed_users, list):
            return email in {
                addr.strip() if isinstance(addr, str) else addr
                for addr in self.allowed_users
            }

        # Handle custom validation function
        if callable(self.allowed_users):
            return self.allowed_users(token)

        raise TypeError(
            "allowed_users must be one of: "
            "str ('all' or email), "
            "list of emails, "
            "or callable taking token dict"
        )

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
