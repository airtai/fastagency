import subprocess
from pathlib import Path

from create_api_docs import _generate_api_docs_for_module


def _run_command_help(command: list[str]) -> str:
    """Run the CLI command with --help and capture the output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


def _generate_cli_docs(cli_name: str, docs_path: Path) -> None:
    """Generate CLI usage documentation for the main CLI and subcommands."""
    cli_help_output = _run_command_help([cli_name, "--help"])

    # Save main CLI help output to a file
    main_help_file = docs_path / "cli_usage.md"
    main_help_file.write_text(f"# {cli_name} CLI Usage\n\n```\n{cli_help_output}\n```")

    # Define the subcommands you want to capture help for
    subcommands = ["run", "dev", "version"]

    # Generate and save documentation for each subcommand
    for subcommand in subcommands:
        subcommand_help_output = _run_command_help([cli_name, subcommand, "--help"])
        subcommand_file = docs_path / f"cli_{subcommand}_usage.md"
        subcommand_file.write_text(
            f"## {cli_name} {subcommand} Usage\n\n```\n{subcommand_help_output}\n```"
        )


def create_api_docs(
    root_path: Path,
    module: str,
) -> None:
    """Create API documentation and CLI usage documentation for a module.

    Args:
        root_path: The root path of the project.
        module: The name of the module.
    """
    # Generate API documentation
    api = _generate_api_docs_for_module(root_path, module)

    docs_dir = root_path / "docs"

    # Generate CLI usage documentation
    _generate_cli_docs(module, docs_dir)

    # Read summary template from file
    navigation_template = (docs_dir / "navigation_template.txt").read_text()

    summary = navigation_template.format(api=api)

    summary = "\n".join(filter(bool, (x.rstrip() for x in summary.split("\n"))))

    (docs_dir / "SUMMARY.md").write_text(summary)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    create_api_docs(root, "fastagency")
