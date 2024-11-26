from functools import wraps
from inspect import signature, Parameter
from typing import Annotated

from fastagency.api.code_injection import inject_params


def test_code_injection() -> None:
    def f(city: Annotated[str, "City name"], date: Annotated[str, "Date"]) -> Annotated[str, "Weather"]:
        return f"{city} {date}"

    # how to remove the city parameter from the signature of g?
    @wraps(f)
    def g(*args, **kwargs):
        return f(city="Zagreb", **kwargs)

    # Update the signature of g to remove the city parameter
    sig = signature(f)
    new_params = [param for name, param in sig.parameters.items() if name != "city"]
    g.__signature__ = sig.replace(parameters=new_params)

    assert list(signature(g).parameters.keys()) == ["date"]

    city="Zagreb"
    ctx = {"city": city, "whatever": "whatever"}
    g = inject_params(f, ctx)
    city = "Split"
    assert list(signature(g).parameters.keys()) == ["date"]
    assert g(date="2021-01-01") == 'Zagreb 2021-01-01'