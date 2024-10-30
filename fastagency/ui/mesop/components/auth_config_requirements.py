from enum import Enum


class ServiceType(Enum):
    FIREBASE = "firebase"


class SignInMethodType(Enum):
    GOOGLE = "google"


# Each service and its allowed sign-in methods
ALLOWED_SIGN_IN_METHODS: dict[ServiceType, frozenset[SignInMethodType]] = {
    ServiceType.FIREBASE: frozenset({SignInMethodType.GOOGLE})
}

# Service-specific configuration requirements
SERVICE_CONFIG_REQUIREMENTS: dict[ServiceType, frozenset[str]] = {
    ServiceType.FIREBASE: frozenset(
        {
            "apiKey",
            "authDomain",
            "projectId",
            "storageBucket",
            "messagingSenderId",
            "appId",
        }
    )
}
