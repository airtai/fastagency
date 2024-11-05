from dataclasses import dataclass
from typing import Any, Callable

import mesop.labs as mel

MEL_WEB_COMPONENT_PATH = (
    "/__fast_agency_internal__/javascript/firebase_auth_component.js"
)


@dataclass
class FirebaseConfig:
    api_key: str
    auth_domain: str
    project_id: str
    storage_bucket: str
    messaging_sender_id: str
    app_id: str


@mel.web_component(path=MEL_WEB_COMPONENT_PATH)  # type: ignore[misc]
def firebase_auth_component(
    on_auth_changed: Callable[[mel.WebEvent], Any], config: FirebaseConfig
) -> Any:
    return mel.insert_web_component(
        name="firebase-auth-component",
        events={
            "authChanged": on_auth_changed,
        },
        properties={
            "apiKey": config.api_key,
            "authDomain": config.auth_domain,
            "projectId": config.project_id,
            "storageBucket": config.storage_bucket,
            "messagingSenderId": config.messaging_sender_id,
            "appId": config.app_id,
        },
    )
