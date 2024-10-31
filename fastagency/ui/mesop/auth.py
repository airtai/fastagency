from typing import Protocol

import mesop as me

__all__ = ["AuthProtocol"]


class AuthProtocol(Protocol):
    def create_security_policy(
        self, policy: me.SecurityPolicy
    ) -> me.SecurityPolicy: ...

    # maybe me.Component is wrong
    def auth_component(self) -> me.component: ...