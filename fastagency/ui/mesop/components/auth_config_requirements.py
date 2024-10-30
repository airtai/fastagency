from enum import Enum
from typing import FrozenSet, Dict

class ServiceType(Enum):
    FIREBASE = "firebase"

class SignInMethodType(Enum):
    GOOGLE = "google"

# Each service and its allowed sign-in methods
ALLOWED_SIGN_IN_METHODS: Dict[ServiceType, FrozenSet[SignInMethodType]] = {
    ServiceType.FIREBASE: frozenset({SignInMethodType.GOOGLE})
}

# Service-specific configuration requirements
SERVICE_CONFIG_REQUIREMENTS: Dict[ServiceType, FrozenSet[str]] = {
    ServiceType.FIREBASE: frozenset({
        "apiKey", 
        "authDomain", 
        "projectId", 
        "storageBucket", 
        "messagingSenderId", 
        "appId"
    })
}
