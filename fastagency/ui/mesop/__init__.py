import sys

from ...exceptions import FastAgencyCLIPythonVersionError

if sys.version_info < (3, 10):
    raise FastAgencyCLIPythonVersionError("Mesop requires Python 3.10 or higher")

from .base import MesopUI

__all__ = ["MesopUI"]
