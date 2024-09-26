import sys

import pytest

from fastagency.exceptions import FastAgencyCLIPythonVersionError


@pytest.mark.skipif(sys.version_info > (3, 9), reason="Python 3.9 or lower is required")
def test_import_below_python_3_10() -> None:
    with pytest.raises(  # noqa: PT012
        FastAgencyCLIPythonVersionError, match="Mesop requires Python 3.10 or higher"
    ):
        from fastagency.ui.mesop import MesopUI

        assert MesopUI is not None
