from typing import Any, Callable, Optional

import mesop.labs as mel

MEL_WEB_COMPONENT_PATH = (
    "/__fast_agency_internal__/javascript/username_password_auth_component.js"
)


@mel.web_component(path=MEL_WEB_COMPONENT_PATH)  # type: ignore[misc]
def username_password_auth_component(
    on_auth_changed: Callable[[mel.WebEvent], Any],
    authenticated_user: Optional[str] = None,
) -> Any:
    return mel.insert_web_component(
        name="username-password-auth-component",
        events={
            "authChanged": on_auth_changed,
        },
        properties={"authenticatedUser": authenticated_user},
    )
