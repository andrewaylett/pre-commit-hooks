"""Fixtures for uv-run hook tests."""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def create_file():
    """Create a test file in the given temporary directory.

    Returns:
        function: A function that creates a file with the given content.
    """

    def _create_file(content, temp_dir, filename):
        file_path = Path(temp_dir) / filename
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    return _create_file


@pytest.fixture
def simple_script_content():
    """Return content for a simple Python script."""
    return """
print("Hello from simple script!")
"""


@pytest.fixture
def failing_script_content():
    """Return content for a failing Python script."""
    return """
import sys
print("This script will fail!")
sys.exit(1)
"""


@pytest.fixture
def simple_script(temp_dir, simple_script_content, create_file):
    """Create a simple Python script in the temporary directory."""
    return create_file(simple_script_content, temp_dir, "simple_script.py")


@pytest.fixture
def failing_script(temp_dir, failing_script_content, create_file):
    """Create a failing Python script in the temporary directory."""
    return create_file(failing_script_content, temp_dir, "failing_script.py")


@pytest.fixture
def git_repo(temp_dir):
    """Set up a git repository in the given temporary directory."""
    # Initialize git repository
    subprocess.run(["git", "init"], cwd=temp_dir, check=True, capture_output=True)

    # Configure git user
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=temp_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=temp_dir,
        check=True,
        capture_output=True,
    )

    # Create .pre-commit-config.yaml
    pre_commit_config = """
repos:
"""
    with open(Path(temp_dir) / ".pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)

    return temp_dir
