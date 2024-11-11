import typing

import bcrypt
import mesop as me
import mesop.labs as mel

from ...data_model import State
from ...styles import MesopHomePageStyles
from .username_password_auth_component import username_password_auth_component

if typing.TYPE_CHECKING:
    from ..auth import AuthProtocol


class UsernamePasswordAuth:  # implements AuthProtocol
    def __init__(self, allowed_users: dict[str, str]) -> None:
        """Initialize the authentication component with allowed users.

        Args:
        allowed_users (dict[str, str]): A dictionary where the keys are usernames and the values are passwords.

        Initializes:
        _self (AuthProtocol): Ensures the instance conforms to the AuthProtocol interface.
        _user_hashes (dict[str, str]): A dictionary where the keys are usernames and the values are hashed passwords.
        """
        # mypy check if self is AuthProtocol
        _self: AuthProtocol = self

        self._user_hashes = {
            username: self._hash_password(password)
            for username, password in allowed_users.items()
        }

    def _hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def create_security_policy(self, policy: me.SecurityPolicy) -> me.SecurityPolicy:
        return policy

    def _verify_password(self, password: str, password_hash: bytes) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash)

    def is_authorized(self, username: str, password: str) -> bool:
        if username not in self._user_hashes:
            raise ValueError("Invalid username or password")

        if not self._verify_password(password, self._user_hashes[username]):
            raise ValueError("Invalid username or password")

        return True

    def on_auth_changed(self, e: mel.WebEvent) -> None:
        state = me.state(State)

        if e.value is None:
            state.authenticated_user = ""
            return

        username, password = e.value["username"], e.value["password"]

        try:
            if not self.is_authorized(username, password):
                raise me.MesopUserException(
                    "You are not authorized to access this application. "
                    "Please contact the application administrators for access."
                )
        except ValueError as e:
            raise me.MesopUserException(str(e)) from e

        state.authenticated_user = username

    # maybe me.Component is wrong
    def auth_component(self) -> me.component:
        styles = MesopHomePageStyles()
        state = me.state(State)
        if state.authenticated_user:
            with me.box(style=styles.logout_btn_container):
                username_password_auth_component(
                    on_auth_changed=self.on_auth_changed,
                    authenticated_user=state.authenticated_user,
                )
        else:
            with me.box(style=styles.login_box):  # noqa: SIM117
                with me.box(style=styles.login_btn_container):
                    me.text("Sign in to your account", style=styles.header_text)
                    username_password_auth_component(
                        on_auth_changed=self.on_auth_changed,
                        authenticated_user=state.authenticated_user,
                    )
