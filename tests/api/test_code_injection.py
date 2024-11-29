from inspect import signature
from typing import Annotated, Any

from fastagency.api.dependency_injection import inject_params


def test_dependency_injection() -> None:
    def f(
        city: Annotated[str, "City name"],
        date: Annotated[str, "Date"],
        user_id: Annotated[int, "User ID"],
    ) -> Annotated[str, "Weather"]:
        return f"User {user_id}: {city} {date}"

    ctx: dict[str, Any] = {"user_id": 123}
    g = inject_params(f, ctx)
    assert list(signature(g).parameters.keys()) == ["city", "date"]
    kwargs: dict[str, Any] = {"city": "Zagreb", "date": "2021-01-01"}
    assert g(**kwargs) == "User 123: Zagreb 2021-01-01"
