import platform
import subprocess
from typing import Any

import pytest
from typer.testing import CliRunner

from fastagency.cli import app

runner = CliRunner()


@pytest.mark.parametrize(
    "command,expected",  # noqa: PT006
    [
        (
            ["docker", "build"],
            [
                "docker",
                "build",
                "-t",
                "deploy_fastagency",
                "-f",
                "docker/Dockerfile",
                "--progress",
                "plain",
                ".",
            ],
        ),
        (
            ["docker", "build", "--no-cache", "."],
            [
                "docker",
                "build",
                "-t",
                "deploy_fastagency",
                "-f",
                "docker/Dockerfile",
                "--progress",
                "plain",
                "--no-cache",
                ".",
            ],
        ),
    ],
)
def test_docker_build(
    command: list[str], expected: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def patch_subprocess_run(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
        assert args[0] == expected
        assert kwargs["check"]
        assert kwargs["capture_output"]
        assert kwargs["text"]

        return subprocess.CompletedProcess(
            args=command, returncode=0, stdout="Dummy docker build output"
        )

    monkeypatch.setattr(subprocess, "run", patch_subprocess_run)

    result = runner.invoke(app, command)
    assert result.exit_code == 0
    assert "Building FastAgency Docker image" in result.stdout
    assert " ".join(expected) in result.stdout


def test_docker_build_invalid_argument(monkeypatch: pytest.MonkeyPatch) -> None:
    command = ["docker", "build", "--invalid-argument", "."]

    if platform.system() == "Windows" or platform.system() == "Darwin":

        def patch_subprocess_run(*args: Any, **kwargs: Any) -> None:
            raise subprocess.CalledProcessError(
                returncode=1,
                cmd=command,
                output="Building FastAgency Docker image and Error: unknown flag: --invalid-argument",
            )

        monkeypatch.setattr(
            subprocess,
            "run",
            patch_subprocess_run,
        )

    result = runner.invoke(app, command)
    assert result.exit_code != 0
    assert "Building FastAgency Docker image" in result.stdout, result.stdout
    assert "Error: unknown flag: --invalid-argument" in result.stdout, result.stdout


@pytest.mark.parametrize(
    "command,expected",  # noqa: PT006
    [
        (
            ["docker", "run"],
            [
                "docker",
                "run",
                "--name",
                "deploy_fastagency",
                "--detach",
                "deploy_fastagency",
            ],
        ),
        (
            ["docker", "run", "--rm"],
            [
                "docker",
                "run",
                "--name",
                "deploy_fastagency",
                "--rm",
                "--detach",
                "deploy_fastagency",
            ],
        ),
        (
            ["docker", "run", "--network", "host"],
            [
                "docker",
                "run",
                "--name",
                "deploy_fastagency",
                "--detach",
                "--network",
                "host",
                "deploy_fastagency",
            ],
        ),
    ],
)
def test_docker_run(
    command: list[str], expected: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def patch_subprocess_run(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
        assert args[0] == expected
        assert kwargs["check"]
        assert kwargs["capture_output"]
        assert kwargs["text"]

        return subprocess.CompletedProcess(
            args=command, returncode=0, stdout="Dummy docker run output"
        )

    monkeypatch.setattr(subprocess, "run", patch_subprocess_run)

    result = runner.invoke(app, command)
    assert result.exit_code == 0
    assert "Running FastAgency Docker image" in result.stdout
    assert " ".join(expected) in result.stdout


def test_docker_run_invalid_argument(monkeypatch: pytest.MonkeyPatch) -> None:
    command = ["docker", "run", "--invalid-argument"]

    if platform.system() == "Windows" or platform.system() == "Darwin":

        def patch_subprocess_run(*args: Any, **kwargs: Any) -> None:
            raise subprocess.CalledProcessError(
                returncode=1,
                cmd=command,
                output="Running FastAgency Docker image and Error: unknown flag: --invalid-argument",
            )

        monkeypatch.setattr(
            subprocess,
            "run",
            patch_subprocess_run,
        )

    result = runner.invoke(app, command)
    assert result.exit_code != 0
    assert "Running FastAgency Docker image" in result.stdout, result.stdout
    assert "Error: unknown flag: --invalid-argument" in result.stdout, result.stdout
