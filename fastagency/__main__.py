"""CLI entry point to FastAgency library."""

import warnings

from .cli import app as cli

warnings.filterwarnings("default", category=ImportWarning, module="fastagency")

if __name__ == "__main__":
    cli(prog_name="fastagency")
