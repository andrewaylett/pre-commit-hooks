"""Tests for file operations in the init-hooks pre-commit hook."""

from pathlib import Path

import pytest
import yaml

from andrewaylett_pre_commit_hooks.init_hooks import (
    ensure_file_exists,
    read_yaml_file,
    write_yaml_file,
)

# Mark all tests in this module to change directory
pytestmark = pytest.mark.change_dir


def test_read_yaml_file(temp_dir, pre_commit_config_file, partial_pre_commit_config):
    """Test that read_yaml_file correctly reads a YAML file."""
    # Read the YAML file
    config = read_yaml_file(str(pre_commit_config_file))

    # Check that the config matches the expected value
    assert config == partial_pre_commit_config


def test_write_yaml_file(temp_dir):
    """Test that write_yaml_file correctly writes a YAML file."""
    # Create a test config
    test_config = {"test": "value"}

    # Write the config to a file
    file_path = Path(temp_dir) / "test.yaml"
    new_file = write_yaml_file(str(file_path), test_config)

    # Check that the write was successful
    assert new_file is True
    assert file_path.exists()

    # Read the file back and check the content
    with open(file_path) as f:
        content = yaml.safe_load(f)
    assert content == test_config


def test_ensure_file_exists_new_file(temp_dir):
    """Test that ensure_file_exists creates a new file with the default content."""
    # Define a test file path
    file_path = Path(temp_dir) / "test.txt"
    test_content = "Test content\n"

    # Ensure the file exists
    new_file = ensure_file_exists(str(file_path), test_content)

    # Check that the operation was successful
    assert new_file is True
    assert file_path.exists()

    # Check that the file has the expected content
    with open(file_path) as f:
        content = f.read()
    assert content == test_content


def test_ensure_file_exists_existing_file(temp_dir):
    """Test that ensure_file_exists leaves an existing file unchanged."""
    # Create a test file
    file_path = Path(temp_dir) / "test.txt"
    original_content = "Original content\n"
    with open(file_path, "w") as f:
        f.write(original_content)

    # Ensure the file exists
    test_content = "Test content\n"
    new_file = ensure_file_exists(str(file_path), test_content)

    # Check that the operation was successful but no file was created
    assert new_file is False

    # Check that the file content is unchanged
    with open(file_path) as f:
        content = f.read()
    assert content == original_content


@pytest.fixture
def partial_pre_commit_config():
    """Return a pre-commit config with some hooks but not all."""
    return {
        "repos": [
            {
                "repo": "https://github.com/pre-commit/pre-commit-hooks",
                "rev": "v4.0.0",
                "hooks": [
                    {"id": "trailing-whitespace"},
                    {"id": "end-of-file-fixer"},
                ],
            }
        ]
    }


@pytest.fixture
def pre_commit_config_file(temp_dir, partial_pre_commit_config):
    """Create a pre-commit config file in the temporary directory."""
    from pathlib import Path

    file_path = Path(temp_dir) / ".pre-commit-config.yaml"
    with open(file_path, "w") as f:
        yaml.dump(partial_pre_commit_config, f)
    return file_path
