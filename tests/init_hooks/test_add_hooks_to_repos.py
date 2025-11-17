"""Tests for the add_hooks_to_repos function in the init-hooks pre-commit hook."""

import pytest

from andrewaylett_pre_commit_hooks.init_hooks import (
    PreCommitHook,
    PreCommitRepo,
    add_hooks_to_repos,
)

# Mark all tests in this module to change directory
pytestmark = pytest.mark.change_dir


def test_add_hooks_to_empty_repos():
    """Test adding hooks to empty repos list."""
    # Setup
    repos: list[PreCommitRepo] = []
    existing_repos = {}
    hooks_dict = {"https://github.com/example/repo": ["hook1", "hook2"]}

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict)

    # Verify
    assert result is True  # Should be mutated
    assert len(repos) == 1
    assert repos[0]["repo"] == "https://github.com/example/repo"
    assert len(repos[0]["hooks"]) == 2
    assert repos[0]["hooks"][0]["id"] == "hook1"
    assert repos[0]["hooks"][1]["id"] == "hook2"
    assert "https://github.com/example/repo" in existing_repos


def test_add_hooks_to_existing_repo():
    """Test adding hooks to an existing repository."""
    # Setup
    repos: list[PreCommitRepo] = [
        {
            "repo": "https://github.com/example/repo",
            "rev": "main",
            "hooks": [{"id": "existing-hook"}],
        }
    ]
    existing_repos = {"https://github.com/example/repo": repos[0]}
    hooks_dict = {"https://github.com/example/repo": ["new-hook", "another-hook"]}

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict)

    # Verify
    assert result is True  # Should be mutated
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 3
    hook_ids = [hook["id"] for hook in repos[0]["hooks"]]
    assert "existing-hook" in hook_ids
    assert "new-hook" in hook_ids
    assert "another-hook" in hook_ids


def test_add_hooks_with_dict_format():
    """Test adding hooks with dictionary format."""
    # Setup
    repos = []
    existing_repos = {}
    hooks_dict: dict[str, list[str | PreCommitHook]] = {
        "https://github.com/example/repo": [
            {"id": "hook1", "args": ["--arg1", "--arg2"]},
            {"id": "hook2", "stages": ["commit"]},
        ]
    }

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict)

    # Verify
    assert result is True  # Should be mutated
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 2
    assert repos[0]["hooks"][0]["id"] == "hook1"
    assert repos[0]["hooks"][0]["args"] == ["--arg1", "--arg2"]
    assert repos[0]["hooks"][1]["id"] == "hook2"
    assert repos[0]["hooks"][1]["stages"] == ["commit"]


def test_add_hooks_mixed_format():
    """Test adding hooks with mixed string and dictionary format."""
    # Setup
    repos = []
    existing_repos = {}
    hooks_dict: dict[str, list[str | PreCommitHook]] = {
        "https://github.com/example/repo": [
            "simple-hook",
            {"id": "complex-hook", "args": ["--arg"]},
        ]
    }

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict)

    # Verify
    assert result is True  # Should be mutated
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 2
    assert repos[0]["hooks"][0]["id"] == "simple-hook"
    assert repos[0]["hooks"][1]["id"] == "complex-hook"
    assert repos[0]["hooks"][1]["args"] == ["--arg"]


def test_add_hooks_to_repo_without_hooks():
    """Test adding hooks to a repository that exists but has no hooks."""
    # Setup
    repos: list[PreCommitRepo] = [
        {
            "repo": "https://github.com/example/repo",
            "rev": "main",
            # No hooks key
        }
    ]
    existing_repos = {"https://github.com/example/repo": repos[0]}
    hooks_dict = {"https://github.com/example/repo": ["hook1", "hook2"]}

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict)

    # Verify
    assert result is True  # Should be mutated
    assert len(repos) == 1
    assert "hooks" in repos[0]
    assert len(repos[0]["hooks"]) == 2
    assert repos[0]["hooks"][0]["id"] == "hook1"
    assert repos[0]["hooks"][1]["id"] == "hook2"


def test_add_hooks_no_mutation_needed():
    """Test that no mutation occurs when all hooks already exist."""
    # Setup
    repos: list[PreCommitRepo] = [
        {
            "repo": "https://github.com/example/repo",
            "rev": "main",
            "hooks": [{"id": "hook1"}, {"id": "hook2"}],
        }
    ]
    existing_repos = {"https://github.com/example/repo": repos[0]}
    hooks_dict = {"https://github.com/example/repo": ["hook1", "hook2"]}

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict)

    # Verify
    assert result is False  # Should not be mutated
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 2


def test_add_hooks_with_hook_type():
    """Test adding hooks with a hook type for logging."""
    # Setup
    repos = []
    existing_repos = {}
    hooks_dict = {"https://github.com/example/repo": ["hook1"]}

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict, hook_type="test")

    # Verify
    assert result is True  # Should be mutated
    assert len(repos) == 1
    assert repos[0]["repo"] == "https://github.com/example/repo"
    assert len(repos[0]["hooks"]) == 1
    assert repos[0]["hooks"][0]["id"] == "hook1"


def test_add_hooks_empty_hooks_dict():
    """Test adding hooks with an empty hooks dictionary."""
    # Setup
    repos = []
    existing_repos = {}
    hooks_dict = {}

    # Execute
    result = add_hooks_to_repos(repos, existing_repos, hooks_dict)

    # Verify
    assert result is False  # Should not be mutated
    assert len(repos) == 0
