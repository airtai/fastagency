from .auth_config_requirements import (
    ALLOWED_SIGN_IN_METHODS,
    SERVICE_CONFIG_REQUIREMENTS,
    ServiceType,
    SignInMethodType,
)

__all__ = ["ServiceType", "SignInMethodType"]


class Auth:
    def __init__(
        self,
        service: ServiceType,
        sign_in_methods: set[SignInMethodType],
        config: dict[str, str],
    ) -> None:
        self.service = service
        self.sign_in_methods = frozenset(sign_in_methods)
        self.config = config

    def __post_init__(self) -> None:
        """Validate the configuration based on the selected service."""
        if not self.sign_in_methods:
            raise ValueError("At least one sign-in method must be specified")

        # Check if valid sign in method is passed for the selected service
        allowed_sign_in_methods = ALLOWED_SIGN_IN_METHODS[self.service]
        if not self.sign_in_methods.issubset(allowed_sign_in_methods):
            raise ValueError(
                f"Invalid sign-in methods for {self.service.value}. "
                f"Allowed methods: {[m.value for m in allowed_sign_in_methods]}"
            )

        # Check if config contains all required keys
        required_keys = SERVICE_CONFIG_REQUIREMENTS.get(self.service)
        if required_keys and not required_keys.issubset(self.config.keys()):
            raise ValueError(
                f"{self.service.value} config must contain: {required_keys}"
            )
