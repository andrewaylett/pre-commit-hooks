"""Tests for the cog pre-commit hook using simulated repositories."""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def project_dir():
    """Return the absolute path to the project directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


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

    # Install pre-commit
    subprocess.run(
        ["uvx", "pre-commit", "install"], cwd=temp_dir, check=True, capture_output=True
    )

    return temp_dir


@pytest.fixture
def passing_content():
    """Return content for a file with cog markers and correctly generated content."""
    return """
def example_passing():
    # [ [ [cog
    # import cog
    # cog.outl("    print('Generated Passing')")
    # ]]]
    print('Generated Passing')
    # [[[end]]]
    pass
""".replace("[ [ [", "[[[")


@pytest.fixture
def failing_content():
    """Return content for a file with cog markers and incorrectly generated content."""
    return """
def example_failing():
    # [ [ [cog
    # import cog
    # cog.outl("    print('Generated Failing')")
    # ]]]
    print('Wrong content')
    # [[[end]]]
    pass
""".replace("[ [ [", "[[[")


@pytest.fixture
def create_file():
    """Create a test file in the given temporary directory."""

    def _create_file(content, temp_dir, filename):
        file_path = Path(temp_dir) / filename
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    return _create_file


def test_passing_repository(git_repo, passing_content, create_file, project_dir):
    """Test that a repository with correctly generated cog content passes the pre-commit check."""
    # Create a file with cog markers and correctly generated content
    create_file(passing_content, git_repo, "with_cog.py")

    # Create .cogfiles listing the files to process
    with open(Path(git_repo) / ".cogfiles", "w") as f:
        f.write("with_cog.py\n")

    # Add the files to git
    subprocess.run(
        ["git", "add", "with_cog.py", ".cogfiles"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )

    # Run pre-commit try-repo
    result = subprocess.run(
        ["uvx", "pre-commit", "try-repo", project_dir, "cog", "--all-files"],
        cwd=git_repo,
        capture_output=True,
        text=True,
    )

    # Check that pre-commit passed
    assert result.returncode == 0, f"Pre-commit failed with error: {result.stderr}"
    assert "Passed" in result.stdout


def test_failing_repository(git_repo, failing_content, create_file, project_dir):
    """Test that a repository with incorrectly generated cog content gets fixed by the pre-commit hook."""
    # Create a file with cog markers and incorrectly generated content
    cog_file = create_file(failing_content, git_repo, "with_cog.py")

    # Save the original content for comparison
    with open(cog_file) as f:
        original_content = f.read()

    # Create .cogfiles listing the files to process
    with open(Path(git_repo) / ".cogfiles", "w") as f:
        f.write("with_cog.py\n")

    # Add the files to git
    subprocess.run(
        ["git", "add", "with_cog.py", ".cogfiles"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )

    # Run pre-commit try-repo with verbose output
    result = subprocess.run(
        [
            "uvx",
            "pre-commit",
            "try-repo",
            project_dir,
            "cog",
            "--all-files",
            "--verbose",
        ],
        cwd=git_repo,
        capture_output=True,
        text=True,
    )

    print(f"Pre-commit stdout: {result.stdout}")
    print(f"Pre-commit stderr: {result.stderr}")

    # Check that pre-commit ran successfully (may return non-zero if files were modified)
    assert (
        "files were modified by this hook" in result.stdout or result.returncode == 0
    ), f"Pre-commit failed with error: {result.stderr}"

    # Read the file after running cog
    with open(cog_file) as f:
        processed_content = f.read()

    # Check that the content was updated by running cog
    assert "print('Generated Failing')" in processed_content, (
        "Cog did not update the content correctly"
    )

    assert original_content != processed_content, (
        "Content was not changed by running cog"
    )


def test_mixed_repository(
    git_repo, passing_content, failing_content, create_file, project_dir
):
    """Test a repository with both passing and failing files."""
    # Create a file with cog markers and correctly generated content
    passing_file = create_file(passing_content, git_repo, "passing.py")

    # Save the original passing content for comparison
    with open(passing_file) as f:
        original_passing = f.read()

    # Create a file with cog markers and incorrectly generated content
    failing_file = create_file(failing_content, git_repo, "failing.py")

    # Save the original failing content for comparison
    with open(failing_file) as f:
        original_failing = f.read()

    # Create .cogfiles listing the files to process
    with open(Path(git_repo) / ".cogfiles", "w") as f:
        f.write("passing.py\nfailing.py\n")

    # Add the files to git
    subprocess.run(
        ["git", "add", "passing.py", "failing.py", ".cogfiles"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )

    # Run pre-commit try-repo with verbose output
    result = subprocess.run(
        [
            "uvx",
            "pre-commit",
            "try-repo",
            project_dir,
            "cog",
            "--all-files",
            "--verbose",
        ],
        cwd=git_repo,
        capture_output=True,
        text=True,
    )

    print(f"Pre-commit stdout: {result.stdout}")
    print(f"Pre-commit stderr: {result.stderr}")

    # Check that pre-commit ran successfully (may return non-zero if files were modified)
    assert (
        "files were modified by this hook" in result.stdout or result.returncode == 0
    ), f"Pre-commit failed with error: {result.stderr}"

    # Read the files after running cog directly
    with open(passing_file) as f:
        passing_processed = f.read()

    with open(failing_file) as f:
        failing_processed = f.read()

    # Check that the content was updated correctly
    assert "print('Generated Passing')" in passing_processed, (
        "Passing file content was not preserved"
    )
    assert "print('Generated Failing')" in failing_processed, (
        "Cog did not update the failing file correctly"
    )

    # Verify that the passing file was not changed (it was already correct)
    assert original_passing == passing_processed, (
        "Passing file was changed when it shouldn't have been"
    )

    # Verify that the failing file was changed
    assert original_failing != failing_processed, (
        "Failing file was not changed by running cog directly"
    )
