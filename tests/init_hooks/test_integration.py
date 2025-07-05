"""Integration tests for the init-hooks pre-commit hook."""

from pathlib import Path

import pytest
import yaml

from andrewaylett_pre_commit_hooks.init_hooks import (
    DEFAULT_EDITORCONFIG,
    DEFAULT_GITIGNORE,
    DEFAULT_YAMLFMT,
    main,
)

# Mark all tests in this module to change directory
pytestmark = pytest.mark.change_dir


def test_main(temp_dir):
    """Test the main function."""
    # Run the main function
    main()

    # Check that the required files exist
    assert Path(temp_dir, ".editorconfig").exists()
    assert Path(temp_dir, ".yamlfmt.yaml").exists()
    assert Path(temp_dir, ".gitignore").exists()
    assert Path(temp_dir, ".pre-commit-config.yaml").exists()

    # Check that the .editorconfig file has the expected content
    with open(Path(temp_dir, ".editorconfig")) as f:
        content = f.read()
    assert content == DEFAULT_EDITORCONFIG

    # Check that the .yamlfmt.yaml file has the expected content
    with open(Path(temp_dir, ".yamlfmt.yaml")) as f:
        content = f.read()
    assert content == DEFAULT_YAMLFMT

    # Check that the .gitignore file has the expected content
    with open(Path(temp_dir, ".gitignore")) as f:
        content = f.read()
    assert content == DEFAULT_GITIGNORE

    # Check that the .pre-commit-config.yaml file has been initialized
    with open(Path(temp_dir, ".pre-commit-config.yaml")) as f:
        config = yaml.safe_load(f)
    assert "repos" in config
    assert len(config["repos"]) > 0
