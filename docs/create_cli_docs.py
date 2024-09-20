import re
import subprocess
from pathlib import Path

from create_api_docs import get_navigation_template

CLI_REFERENCE_PATH = "cli"


def _run_command_generate_docs(output_path: Path) -> str:
    """Run the CLI command with --help and capture the output."""
    result = subprocess.run(
        ["typer", "fastagency.cli", "utils", "docs", "--name", "fastagency"],
        capture_output=True,
        text=True,
        check=True,
    )

    # replace bold tags with markdown bold
    fix_bold = "\\[bold\\](.*?)\\[/bold\\]"
    retval = re.sub(fix_bold, r"**\1**", result.stdout[:-1])

    # replace link tags with markdown link
    fix_link = "\\[link\\](.*?)\\[/link\\]"
    retval = re.sub(fix_link, r"[\1](\1)", retval)

    # replace color tags with markdown blue (todo: fix me)
    for color in ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]:
        fix_color = f"\\[{color}\\](.*?)\\[/{color}\\]"
        retval = re.sub(fix_color, r"<code>\1</code>", retval)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        f.write(retval)

    return retval


def _generate_cli_docs(
    cli_name: str,
    docs_path: Path,
    cli_dir: str = CLI_REFERENCE_PATH,
    cli_md_name: str = "cli.md",
) -> str:
    _run_command_generate_docs(docs_path / cli_dir / cli_md_name)
    return f"    - [CLI]({cli_dir}/{cli_md_name})"


def create_cli_docs(
    root_path: Path,
    module: str,
    navigation_template: str,
) -> str:
    """Create CLI usage documentation for a module.

    Args:
        root_path: The root path of the project.
        module: The name of the module.
        navigation_template: The navigation template for the documentation.
    """
    docs_dir = root_path / "docs"

    # Generate CLI usage documentation
    cli = _generate_cli_docs(module, docs_dir / "en")

    summary = navigation_template.format(cli=cli, api="{api}")

    summary = "\n".join(filter(bool, (x.rstrip() for x in summary.split("\n"))))

    (docs_dir / "SUMMARY.md").write_text(summary)

    return summary


if __name__ == "__main__":
    root_path = Path(__file__).resolve().parent
    docs_dir = root_path / "docs"

    navigation_template = get_navigation_template(docs_dir)

    create_cli_docs(root_path, "fastagency", navigation_template)
