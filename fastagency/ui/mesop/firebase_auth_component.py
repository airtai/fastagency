from dataclasses import dataclass
from typing import Any, Callable, Optional

import mesop.labs as mel

MEL_WEB_COMPONENT_PATH = (
    "/__fast_agency_internal__/javascript/firebase_auth_component.js"
)


@dataclass
class FirebaseConfig:
    api_key: Optional[str] = None
    auth_domain: Optional[str] = None
    project_id: Optional[str] = None
    storage_bucket: Optional[str] = None
    messaging_sender_id: Optional[str] = None
    app_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Validates the FirebaseConfig instance after initialization to ensure no required fields are null."""
        null_values = [key for key, value in self.__dict__.items() if value is None]
        if null_values:
            raise ValueError(
                f"Error: The following FirebaseConfig fields are null. Please set proper values: {null_values}."
            )


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
