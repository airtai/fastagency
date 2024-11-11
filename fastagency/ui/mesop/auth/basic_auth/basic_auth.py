import typing

import bcrypt
import mesop as me
import mesop.labs as mel

from ...data_model import State
from ...styles import MesopHomePageStyles
from .basic_auth_component import basic_auth_component

if typing.TYPE_CHECKING:
    from ..auth import AuthProtocol


class BasicAuth:  # implements AuthProtocol
    def __init__(self, allowed_users: dict[str, str]) -> None:
        """Initialize the authentication component with allowed users.

        Args:
        allowed_users (dict[str, str]): A dictionary where the keys are usernames and the values are passwords.

        Initializes:
        _self (AuthProtocol): Ensures the instance conforms to the AuthProtocol interface.
        allowed_users (dict[str, str]): A dictionary where the keys are usernames and the values are hashed passwords.
        """
        # mypy check if self is AuthProtocol
        _self: AuthProtocol = self

        self.allowed_users = allowed_users

    def create_security_policy(self, policy: me.SecurityPolicy) -> me.SecurityPolicy:
        return policy

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def is_authorized(self, username: str, password: str) -> bool:
        if username not in self.allowed_users:
            return False

        password_hash = self.allowed_users[username]
        return self._verify_password(password, password_hash)

    def on_auth_changed(self, e: mel.WebEvent) -> None:
        state = me.state(State)

        if e.value is None:
            state.authenticated_user = ""
            return

        username, password = e.value["username"], e.value["password"]

        if not self.is_authorized(username, password):
            raise me.MesopUserException("Invalid username or password")

        state.authenticated_user = username

    # maybe me.Component is wrong
    def auth_component(self) -> me.component:
        styles = MesopHomePageStyles()
        state = me.state(State)
        if state.authenticated_user:
            with me.box(style=styles.logout_btn_container):
                basic_auth_component(
                    on_auth_changed=self.on_auth_changed,
                    authenticated_user=state.authenticated_user,
                )
        else:
            with me.box(style=styles.login_box):  # noqa: SIM117
                with me.box(style=styles.login_btn_container):
                    basic_auth_component(
                        on_auth_changed=self.on_auth_changed,
                        authenticated_user=state.authenticated_user,
                    )
