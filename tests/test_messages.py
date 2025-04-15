from typing import Any, Optional, Union

import pytest

from fastagency.messages import MessageProcessorMixin


class TestMessageProcessorMixin:
    @pytest.mark.parametrize(
        ("body", "expected"),
        [
            ("test", "test"),
            (None, ""),
            ("", ""),
            ([{"type": "text", "text": "Hi"}], "Hi"),
            (
                [{"type": "image", "image": "this-is-image"}],
                "Inserting 'image' content",
            ),
        ],
    )
    def test_body_to_str(
        self, body: Optional[Union[str, list[dict[str, Any]]]], expected: str
    ) -> None:
        result = MessageProcessorMixin._body_to_str(
            body=body,
        )

        assert result == expected
