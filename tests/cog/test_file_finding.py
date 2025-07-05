"""Tests for finding files with cog markers."""

import pytest

from andrewaylett_pre_commit_hooks.cog import find_cog_files

# Mark all tests in this module to change directory
pytestmark = pytest.mark.change_dir


def test_find_cog_files_with_cogfiles(temp_dir, cogfiles_file, cog_file):
    """Test that find_cog_files correctly uses .cogfiles."""
    # Find cog files
    files = find_cog_files()

    # Check that the files listed in .cogfiles are found
    assert len(files) == 1
    assert "with_cog.py" in files


def test_find_cog_files_with_readme_md(temp_dir, readme_md_file):
    """Test that find_cog_files correctly uses README.md when .cogfiles doesn't exist."""
    # Find cog files
    files = find_cog_files()

    # Check that only README.md is found
    assert len(files) == 1
    assert "README.md" in files


def test_find_cog_files_with_readme(temp_dir, readme_file):
    """Test that find_cog_files correctly uses README when .cogfiles and README.md don't exist."""
    # Find cog files
    files = find_cog_files()

    # Check that only README is found
    assert len(files) == 1
    assert "README" in files
