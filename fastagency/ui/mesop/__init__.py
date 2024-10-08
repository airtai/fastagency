import sys

from ...exceptions import FastAgencyCLIPythonVersionError
from ...helpers import check_imports

if sys.version_info < (3, 10):
    raise FastAgencyCLIPythonVersionError("Mesop requires Python 3.10 or higher")

check_imports(["mesop"], "mesop")

from .mesop import MesopUI  # noqa: E402

__all__ = ["MesopUI"]
