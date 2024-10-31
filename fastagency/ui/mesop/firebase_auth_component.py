from typing import Any, Callable

import mesop.labs as mel

MEL_WEB_COMPONENT_PATH = (
    "/__fast_agency_internal__/javascript/firebase_auth_component.js"
)


@mel.web_component(path=MEL_WEB_COMPONENT_PATH)  # type: ignore[misc]
def firebase_auth_component(on_auth_changed: Callable[[mel.WebEvent], Any]) -> Any:
    return mel.insert_web_component(
        name="firebase-auth-component",
        events={
            "authChanged": on_auth_changed,
        },
    )
