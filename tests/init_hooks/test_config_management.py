"""Tests for pre-commit config management in the init-hooks pre-commit hook."""

from pathlib import Path

import pytest
import yaml

from andrewaylett_pre_commit_hooks.init_hooks import (
    DEFAULT_HOOKS,
    ensure_pre_commit_config,
)

# Mark all tests in this module to change directory
pytestmark = pytest.mark.change_dir


@pytest.fixture
def empty_pre_commit_config():
    """Return an empty pre-commit config."""
    return {}


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
    file_path = Path(temp_dir) / ".pre-commit-config.yaml"
    with open(file_path, "w") as f:
        yaml.dump(partial_pre_commit_config, f)
    return file_path


@pytest.fixture
def pre_commit_config_with_comments(temp_dir):
    """Create a pre-commit config file with comments in the temporary directory."""
    file_path = Path(temp_dir) / ".pre-commit-config.yaml"
    content = """# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  # Use the latest version
  rev: v4.0.0
  hooks:
  - id: trailing-whitespace
    # Remove trailing whitespace
  - id: end-of-file-fixer
    # Fix end of files
"""
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_ensure_pre_commit_config_empty(temp_dir, empty_pre_commit_config):
    """Test that ensure_pre_commit_config correctly initializes an empty config."""
    # Define a test file path
    file_path = Path(temp_dir) / ".pre-commit-config.yaml"

    # Write an empty config to the file
    with open(file_path, "w") as f:
        yaml.dump(empty_pre_commit_config, f)

    # Ensure the pre-commit config
    success = ensure_pre_commit_config(str(file_path))

    # Check that the operation was successful
    assert success is True

    # Read the updated config
    with open(file_path) as f:
        config = yaml.safe_load(f)

    # Check that the config has been initialized with the required hooks
    assert "repos" in config
    assert len(config["repos"]) > 0

    # Check that all required repositories are present
    repo_urls = [repo["repo"] for repo in config["repos"]]
    for repo_url in DEFAULT_HOOKS:
        assert repo_url in repo_urls

    # Check that all required hooks are present
    for repo_url, hooks in DEFAULT_HOOKS.items():
        repo = next(repo for repo in config["repos"] if repo["repo"] == repo_url)
        hook_ids = [hook["id"] for hook in repo["hooks"]]
        for hook_id in hooks:
            assert hook_id in hook_ids


def test_ensure_pre_commit_config_partial(
    temp_dir, pre_commit_config_file, partial_pre_commit_config
):
    """Test that ensure_pre_commit_config correctly updates a partial config."""
    # Ensure the pre-commit config
    success = ensure_pre_commit_config(str(pre_commit_config_file))

    # Check that the operation was successful
    assert success is True

    # Read the updated config
    with open(pre_commit_config_file) as f:
        config = yaml.safe_load(f)

    # Check that the config has been updated with the required hooks
    assert "repos" in config
    assert len(config["repos"]) > 0

    # Check that all required repositories are present
    repo_urls = [repo["repo"] for repo in config["repos"]]
    for repo_url in DEFAULT_HOOKS:
        assert repo_url in repo_urls

    # Check that all required hooks are present
    for repo_url, hooks in DEFAULT_HOOKS.items():
        repo = next(repo for repo in config["repos"] if repo["repo"] == repo_url)
        hook_ids = [hook["id"] for hook in repo["hooks"]]
        for hook_id in hooks:
            assert hook_id in hook_ids

    # Check that existing hooks are preserved
    pre_commit_hooks_repo = next(
        repo
        for repo in config["repos"]
        if repo["repo"] == "https://github.com/pre-commit/pre-commit-hooks"
    )
    hook_ids = [hook["id"] for hook in pre_commit_hooks_repo["hooks"]]
    assert "trailing-whitespace" in hook_ids
    assert "end-of-file-fixer" in hook_ids


def test_preserve_comments(temp_dir, pre_commit_config_with_comments):
    """Test that comments in pre-commit config files are preserved."""
    # Ensure the pre-commit config
    success = ensure_pre_commit_config(str(pre_commit_config_with_comments))

    # Check that the operation was successful
    assert success is True

    # Read the updated file content
    with open(pre_commit_config_with_comments) as f:
        updated_content = f.read()

    # Check that the comments are preserved
    assert "# See https://pre-commit.com for more information" in updated_content
    assert "# See https://pre-commit.com/hooks.html for more hooks" in updated_content
    assert "# Use the latest version" in updated_content
    assert "# Remove trailing whitespace" in updated_content
    assert "# Fix end of files" in updated_content
