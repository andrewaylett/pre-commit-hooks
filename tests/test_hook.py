"""Tests for the cog pre-commit hook."""

import os
import tempfile
from pathlib import Path

import pytest

from andrewaylett_pre_commit_hooks.cog import find_cog_files, main, run_cog_on_files


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(original_dir)


@pytest.fixture
def cog_content():
    """Return content for a file with cog markers."""
    return """
def example():
    # [ [ [cog
    # import cog
    # cog.outl("    print('Generated')")
    # ]]]
    # Content will be generated here
    # [[[end]]]
    pass
""".replace("[ [ [", "[[[")


@pytest.fixture
def no_cog_content():
    """Return content for a file without cog markers."""
    return """
def example():
    print("No cog markers here")
    pass
"""


@pytest.fixture
def cog_file(temp_dir, cog_content):
    """Create a test file with cog markers in the temporary directory."""
    file_path = Path(temp_dir) / "with_cog.py"
    with open(file_path, "w") as f:
        f.write(cog_content)
    return file_path


@pytest.fixture
def no_cog_file(temp_dir, no_cog_content):
    """Create a test file without cog markers in the temporary directory."""
    file_path = Path(temp_dir) / "without_cog.py"
    with open(file_path, "w") as f:
        f.write(no_cog_content)
    return file_path


@pytest.fixture
def cogfiles_content():
    """Return content for a .cogfiles file."""
    return """
with_cog.py
"""


@pytest.fixture
def cogfiles_file(temp_dir, cogfiles_content):
    """Create a .cogfiles file in the temporary directory."""
    file_path = Path(temp_dir) / ".cogfiles"
    with open(file_path, "w") as f:
        f.write(cogfiles_content)
    return file_path


@pytest.fixture
def readme_md_file(temp_dir, cog_content):
    """Create a README.md file in the temporary directory."""
    file_path = Path(temp_dir) / "README.md"
    with open(file_path, "w") as f:
        f.write(cog_content)
    return file_path


@pytest.fixture
def readme_file(temp_dir, cog_content):
    """Create a README file in the temporary directory."""
    file_path = Path(temp_dir) / "README"
    with open(file_path, "w") as f:
        f.write(cog_content)
    return file_path


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


def test_run_cog_on_files(cog_file):
    """Test that run_cog_on_files correctly processes files with cog markers."""
    # Run cog on the file
    success = run_cog_on_files({str(cog_file)})

    # Check that cog ran successfully
    assert success is True

    # Read the processed file
    with open(cog_file) as f:
        processed_content = f.read()

    # Check that the cog-generated content is present
    assert "print('Generated')" in processed_content


def test_main_with_cogfiles(temp_dir, cog_file, cogfiles_file):
    """Test the main function with .cogfiles."""
    # Run the main function
    main()

    # Read the processed file
    with open(cog_file) as f:
        processed_content = f.read()

    # Check that the cog-generated content is present
    assert "print('Generated')" in processed_content


def test_main_with_readme_md(temp_dir, readme_md_file):
    """Test the main function with README.md."""
    # Run the main function
    main()

    # Read the processed file
    with open(readme_md_file) as f:
        processed_content = f.read()

    # Check that the cog-generated content is present
    assert "print('Generated')" in processed_content


def test_main_with_readme(temp_dir, readme_file):
    """Test the main function with README."""
    # Run the main function
    main()

    # Read the processed file
    with open(readme_file) as f:
        processed_content = f.read()

    # Check that the cog-generated content is present
    assert "print('Generated')" in processed_content
