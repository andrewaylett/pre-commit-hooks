"""Integration tests for the cog pre-commit hook using simulated repositories."""

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


def test_passing_repository(git_repo, passing_cog_content, create_file, project_dir):
    """Test that a repository with correctly generated cog content passes the pre-commit check."""
    # Create a file with cog markers and correctly generated content
    create_file(passing_cog_content, git_repo, "with_cog.py")

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

    with chdir(git_repo):
        # Run pre-commit try-repo using the module from dev dependencies
        result = pre_commit_main(["try-repo", project_dir, "cog", "--all-files"])

    # Check that pre-commit passed
    assert result == 0, "Pre-commit failed with error"


def test_failing_repository(git_repo, failing_cog_content, create_file, project_dir):
    """Test that a repository with incorrectly generated cog content gets fixed by the pre-commit hook."""
    # Create a file with cog markers and incorrectly generated content
    cog_file = create_file(failing_cog_content, git_repo, "with_cog.py")

    # Save the original content for comparison
    with open(cog_file) as f:
        original_content = f.read()

    # Create .cogfiles listing the files to process
    with open(Path(git_repo) / ".cogfiles", "w") as f:
        f.write("with_cog.py\n")

    with chdir(git_repo):
        # Run pre-commit try-repo using the module from dev dependencies
        result = pre_commit_main(["try-repo", project_dir, "cog", "--all-files"])

    # Check that pre-commit passed
    assert result == 0, "Pre-commit failed with error"

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
    git_repo, passing_cog_content, failing_cog_content, create_file, project_dir
):
    """Test a repository with both passing and failing files."""
    # Create a file with cog markers and correctly generated content
    passing_file = create_file(passing_cog_content, git_repo, "passing.py")

    # Save the original passing content for comparison
    with open(passing_file) as f:
        original_passing = f.read()

    # Create a file with cog markers and incorrectly generated content
    failing_file = create_file(failing_cog_content, git_repo, "failing.py")

    # Save the original failing content for comparison
    with open(failing_file) as f:
        original_failing = f.read()

    # Create .cogfiles listing the files to process
    with open(Path(git_repo) / ".cogfiles", "w") as f:
        f.write("passing.py\nfailing.py\n")

    with chdir(git_repo):
        # Run pre-commit try-repo using the module from dev dependencies
        result = pre_commit_main(["try-repo", project_dir, "cog", "--all-files"])

    # Check that pre-commit passed
    assert result == 0, "Pre-commit failed with error"

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
