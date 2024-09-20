import subprocess
from pathlib import Path

from create_api_docs import get_navigation_template


def _run_command_help(command: list[str]) -> str:
    """Run the CLI command with --help and capture the output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


CLI_INTRO = """The **FastAgency Command Line Interface (CLI)** enables developers to manage and run FastAgency projects directly from the terminal.
The CLI simplifies interactions with FastAgency apps, providing options for running, testing, and managing workflows efficiently."""


def _generate_cli_docs(cli_name: str, docs_path: Path) -> str:
    """Generate CLI usage documentation for the main CLI and subcommands."""
    cli_help_output = _run_command_help([cli_name, "--help"])

    # Save main CLI help output to a file
    main_help_file = docs_path / "fastagency-cli.md"
    main_help_file.write_text(f"# CLI\n\n{CLI_INTRO}\n\n```{cli_help_output}```\n")

    # Define the subcommands you want to capture help for
    subcommands = ["run", "dev", "version"]

    cli_summary = "(cli/fastagency-cli.md)"

    submodule = 2
    indent = " " * 4 * submodule
    # Generate and save documentation for each subcommand
    for subcommand in subcommands:
        subcommand_help_output = _run_command_help([cli_name, subcommand, "--help"])
        file_name = f"fastagency-{subcommand}.md"
        subcommand_file = docs_path / file_name
        subcommand_file.write_text(
            f"## {cli_name} {subcommand} Usage\n\n```{subcommand_help_output}```\n"
        )
        # Uppercase the first letter of the subcommand
        cli_summary += f"\n{indent}- [{subcommand.capitalize()}](cli/{file_name})"

    return cli_summary


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
    cli = _generate_cli_docs(module, docs_dir / "en" / "cli")

    summary = navigation_template.format(cli=cli, api="{api}")

    summary = "\n".join(filter(bool, (x.rstrip() for x in summary.split("\n"))))

    (docs_dir / "SUMMARY.md").write_text(summary)

    return summary


if __name__ == "__main__":
    root_path = Path(__file__).resolve().parent
    docs_dir = root_path / "docs"

    navigation_template = get_navigation_template(docs_dir)

    create_cli_docs(root_path, "fastagency", navigation_template)
