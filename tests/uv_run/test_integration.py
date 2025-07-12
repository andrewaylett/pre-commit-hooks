"""Integration tests for the uv-run pre-commit hook using simulated repositories."""

import os
import subprocess
from contextlib import chdir
from pathlib import Path

import pytest
from pre_commit.main import main as pre_commit_main


@pytest.fixture
def project_dir():
    """Return the absolute path to the project directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


def test_successful_command(git_repo, simple_script, project_dir):
    """Test that a successful command passes the pre-commit check."""
    # Add the script to git
    subprocess.run(
        ["git", "add", "simple_script.py"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )

    # Create a pre-commit config file with the hook and arguments
    pre_commit_config = f"""
repos:
- repo: {project_dir}
  rev: HEAD
  hooks:
  - id: uv-run
    args: ["python", "simple_script.py"]
"""
    with open(Path(git_repo) / ".pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)

    with chdir(git_repo):
        # Run pre-commit with the config file
        result = pre_commit_main(["run", "--all-files"])

    # Check that pre-commit passed
    assert result == 0, "Pre-commit failed with error"


def test_failing_command(git_repo, failing_script, project_dir):
    """Test that a failing command fails the pre-commit check."""
    # Add the script to git
    subprocess.run(
        ["git", "add", "failing_script.py"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )

    # Create a pre-commit config file with the hook and arguments
    pre_commit_config = f"""
repos:
- repo: {project_dir}
  rev: HEAD
  hooks:
  - id: uv-run
    args: ["python", "failing_script.py"]
"""
    with open(Path(git_repo) / ".pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)

    with chdir(git_repo):
        # Run pre-commit with the config file
        result = pre_commit_main(["run", "--all-files"])

    # Check that pre-commit failed
    assert result != 0, "Pre-commit should have failed but didn't"


def test_no_command_args(git_repo, project_dir):
    """Test that running without command arguments fails the pre-commit check."""
    # Create a pre-commit config file with the hook but no arguments
    pre_commit_config = f"""
repos:
- repo: {project_dir}
  rev: HEAD
  hooks:
  - id: uv-run
"""
    with open(Path(git_repo) / ".pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)

    with chdir(git_repo):
        # Run pre-commit with the config file
        result = pre_commit_main(["run", "--all-files"])

    # Check that pre-commit failed
    assert result != 0, "Pre-commit should have failed but didn't"


def test_complex_command(git_repo, project_dir):
    """Test that a more complex command works correctly."""
    # Create a Python script that prints a complex message
    complex_script = """
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print("This is a complex command test")
"""
    with open(Path(git_repo) / "complex_script.py", "w") as f:
        f.write(complex_script)

    # Add the file to git
    subprocess.run(
        ["git", "add", "complex_script.py"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )

    # Create a pre-commit config file with the hook and arguments
    pre_commit_config = f"""
repos:
- repo: {project_dir}
  rev: HEAD
  hooks:
  - id: uv-run
    args: ["python", "complex_script.py"]
"""
    with open(Path(git_repo) / ".pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)

    with chdir(git_repo):
        # Run pre-commit with the config file
        result = pre_commit_main(["run", "--all-files"])

    # Check that pre-commit passed
    assert result == 0, "Pre-commit failed with error"
