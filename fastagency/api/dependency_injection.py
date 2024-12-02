from functools import wraps
from inspect import signature
from typing import Any, Callable


def inject_params(f: Callable[..., Any], ctx: dict[str, Any]) -> Callable[..., Any]:
    keys_used = set(signature(f).parameters.keys()) & set(ctx.keys())

    @wraps(f)
    def wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
        # check if all required parameters are present
        if not keys_used.issubset(ctx.keys()):
            raise ValueError(f"Missing required parameters: {keys_used - ctx.keys()}")

        params = {k: ctx[k] for k in keys_used}
        return f(**params, **kwargs)

    # Update the signature of wrapper to remove parameters passed in kwargs
    sig = signature(f)
    new_params = [
        param for name, param in sig.parameters.items() if name not in keys_used
    ]
    wrapper.__signature__ = sig.replace(parameters=new_params)  # type: ignore[attr-defined]

    return wrapper
