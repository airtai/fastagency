import os.path
import sys

import pytest

if sys.version_info < (3, 10):
    pytest.skip("Mesop is not supported in Python 3.9", allow_module_level=True)
from fastagency.ui.mesop.timer import (
    WINDOWS_MEL_WEB_COMPONENT_PATH,
)

TEST_LINUX_PATH = "/test/random/path"
TEST_WINDOWS_PATH = TEST_LINUX_PATH.replace("/", "\\")


@pytest.mark.skipif(
    sys.version_info < (3, 10), reason="Mesop is not supported in Python 3.9"
)
class TestStrOSPatch:
    @pytest.mark.parametrize(
        "value, startswith, expected",  # noqa: PT006
        [
            (TEST_LINUX_PATH, "/", True),
            (TEST_LINUX_PATH, "\\", False),
            (TEST_WINDOWS_PATH, "/", False),
            (TEST_WINDOWS_PATH, "\\", True),
            ("random string", "r", True),
            ("random string", "/", False),
        ],
    )
    def test_MyStr_startswith(  # noqa: N802
        self, value: str, startswith: str, expected: bool
    ) -> None:
        from fastagency.ui.mesop.timer import (
            MyStr,
        )

        assert MyStr(value).startswith(startswith) == expected

    @pytest.mark.skipif(sys.platform != "win32", reason="Test only runs on Windows")
    def test_MyStr_startswith_windows(self) -> None:  # noqa: N802
        from fastagency.ui.mesop.timer import (
            WINDOWS_MEL_WEB_COMPONENT_PATH,
            MyStr,
        )

        assert MyStr(WINDOWS_MEL_WEB_COMPONENT_PATH).startswith("/")

    @pytest.mark.parametrize(
        "value, expected",  # noqa: PT006
        [
            (TEST_LINUX_PATH, False),
            (WINDOWS_MEL_WEB_COMPONENT_PATH, True),
            ("random string", False),
        ],
    )
    def test_os_path_normpath_patch(self, value: str, expected: bool) -> None:
        from fastagency.ui.mesop.timer import (
            MyStr,
            os_path_normpath_patch,
        )

        actual = os_path_normpath_patch(value)
        assert isinstance(actual, MyStr) == expected

    def test_patch_os_and_str(self) -> None:
        from fastagency.ui.mesop.timer import (
            os_path_normpath_patch,
            patch_os_and_str,
        )

        with patch_os_and_str():
            assert os.path.normpath is os_path_normpath_patch
        assert os.path.normpath is not os_path_normpath_patch
