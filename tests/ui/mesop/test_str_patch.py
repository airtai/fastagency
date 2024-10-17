import os.path
import sys

import pytest

from fastagency.ui.mesop.timer import (
    MEL_WEB_COMPONENT_PATH,
    WINDOWS_MEL_WEB_COMPONENT_PATH,
    MyStr,
    os_path_normpath_patch,
    patch_os_and_str,
)


@pytest.mark.parametrize(
    "value, startswith, expected",  # noqa: PT006
    [
        (MEL_WEB_COMPONENT_PATH, "/", True),
        (MEL_WEB_COMPONENT_PATH, "\\", False),
        (WINDOWS_MEL_WEB_COMPONENT_PATH, "/", False),
        (WINDOWS_MEL_WEB_COMPONENT_PATH, "\\", True),
        ("random string", "r", True),
        ("random string", "/", False),
    ],
)
def test_MyStr_startswith(value: str, startswith: str, expected: bool) -> None:  # noqa: N802
    assert MyStr(value).startswith(startswith) == expected


@pytest.mark.skipif(sys.platform != "win32", reason="Test only runs on Windows")
def test_MyStr_startswith_windows() -> None:  # noqa: N802
    assert MyStr(WINDOWS_MEL_WEB_COMPONENT_PATH).startswith("/")


@pytest.mark.parametrize(
    "value, expected",  # noqa: PT006
    [
        (MEL_WEB_COMPONENT_PATH, False),
        (WINDOWS_MEL_WEB_COMPONENT_PATH, True),
        ("random string", False),
    ],
)
def test_os_path_normpath_patch(value: str, expected: bool) -> None:
    actual = os_path_normpath_patch(value)
    assert isinstance(actual, MyStr) == expected


def test_patch_os_and_str() -> None:
    with patch_os_and_str():
        assert os.path.normpath is os_path_normpath_patch
    assert os.path.normpath is not os_path_normpath_patch
