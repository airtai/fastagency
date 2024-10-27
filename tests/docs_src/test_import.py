import importlib
import sys
from pathlib import Path

import pytest

from fastagency.exceptions import FastAgencyCLIPythonVersionError

from ..helpers import add_to_sys_path, list_submodules

root_path = (Path(__file__).parents[2] / "docs").resolve()
module_name = "docs_src"


def test_list_submodules() -> None:
    # Specify the name of the module you want to inspect

    # Get the list of submodules for the specified module
    submodules = list_submodules(module_name, include_path=root_path)

    assert len(submodules) > 0
    assert "docs_src" in submodules
    assert "docs_src.getting_started" in submodules
    assert "docs_src.getting_started.main_console" in submodules


@pytest.mark.parametrize("module", list_submodules(module_name, include_path=root_path))
def test_submodules(module: str) -> None:
    with add_to_sys_path(root_path):
        if sys.version_info < (3, 10):
            if module == "docs_src.user_guide.ui.mesop.main_mesop":
                with pytest.raises(
                    ModuleNotFoundError,
                    match="No module named 'mesop'",
                ):
                    importlib.import_module(module)
                return
            elif (
                module.startswith("docs_src.user_guide.ui.mesop")
                or module == "docs_src.tutorials.giphy"
                or module == "docs_src.tutorials.whatsapp"
                or module == "docs_src.user_guide.runtimes.autogen.mesop"
            ):
                pass
            elif ("mesop" in module) or ("giphy" in module) or ("whatsapp" in module):
                with pytest.raises(
                    FastAgencyCLIPythonVersionError,
                    match="Mesop requires Python 3.10 or higher",
                ):
                    importlib.import_module(module)
                return

        importlib.import_module(module)
