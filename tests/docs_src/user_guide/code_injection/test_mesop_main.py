import pytest

from docs.docs_src.user_guide.code_injection.mesop_main import get_savings


def test_get_savings() -> None:
    assert get_savings("rba", "token-1-a") == "Your savings: 1000$"


def test_get_savings_raises_exception() -> None:
    with pytest.raises(expected_exception=ValueError, match="Token not found"):
        get_savings("rba", "token-1-c")
