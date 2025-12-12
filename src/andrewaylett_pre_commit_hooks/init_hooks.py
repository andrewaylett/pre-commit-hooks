import os
import sys
from typing import Any, NotRequired, TypedDict

from ruamel.yaml import YAML

from andrewaylett_pre_commit_hooks import error_logger, logger


class PreCommitHook(TypedDict):
    id: str
    args: NotRequired[list[str]]
    stages: NotRequired[list[str]]


class PreCommitRepo(TypedDict):
    repo: str
    rev: str
    hooks: NotRequired[list[PreCommitHook]]


# Default versions for repositories
DEFAULT_REPO_VERSIONS = {
    "https://github.com/pre-commit/pre-commit-hooks": "v6.0.0",
    "https://github.com/google/yamlfmt": "v0.20.0",
    "https://github.com/rhysd/actionlint": "v1.7.9",
    "https://github.com/editorconfig-checker/editorconfig-checker.python": "3.6.0",
    "https://github.com/python-jsonschema/check-jsonschema": "0.35.0",
    "https://github.com/andrewaylett/pre-commit-hooks": "v0.7.1",
    "https://github.com/renovatebot/pre-commit-hooks": "42.50.1",
}

# Default hooks that should be enabled
DEFAULT_HOOKS = {
    "https://github.com/pre-commit/pre-commit-hooks": [
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-case-conflict",
        "check-merge-conflict",
        "check-yaml",
        "check-toml",
        "check-xml",
        "check-added-large-files",
        "forbid-submodules",
        "mixed-line-ending",
    ],
    "https://github.com/google/yamlfmt": [
        "yamlfmt",
    ],
    "https://github.com/editorconfig-checker/editorconfig-checker.python": [
        "editorconfig-checker",
    ],
    "https://github.com/andrewaylett/pre-commit-hooks": [
        "init-hooks",
    ],
}

# Hooks that should be enabled only if .github/workflows directory exists
GITHUB_ACTIONS_HOOKS = {
    "https://github.com/rhysd/actionlint": [
        "actionlint",
    ],
    "https://github.com/python-jsonschema/check-jsonschema": [
        "check-github-workflows",
    ],
}

# Hooks that should be enabled only if renovate.json file exists
RENOVATE_HOOKS: dict[str, list[str | PreCommitHook]] = {
    "https://github.com/python-jsonschema/check-jsonschema": [
        "check-renovate",
    ],
    "https://github.com/renovatebot/pre-commit-hooks": [
        {"id": "renovate-config-validator", "args": ["--strict"]},
    ],
}

# Default content for .editorconfig
DEFAULT_EDITORCONFIG = """[*]
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2
ij_yaml_indent_sequence_value = false

[*.md]
indent_size = unset
"""

# Default content for .yamlfmt.yaml
DEFAULT_YAMLFMT = """formatter:
  type: basic
  indentless_arrays: true
  retain_line_breaks_single: true
  line_breaks: lf
"""

# Default content for .gitignore
DEFAULT_GITIGNORE = """*~
.*.swp
"""

# https://docs.github.com/en/actions/how-tos/managing-workflow-runs-and-deployments/managing-workflow-runs/manage-caches
DEFAULT_ACTIONS_CACHE_CLEANUP = """
name: Cleanup github runner caches on closed pull requests
on:
  pull_request:
    types:
    - closed

jobs:
  cleanup:
    runs-on: ubuntu-latest
    permissions:
      actions: write
    steps:
    - name: Cleanup
      run: |
        echo "Fetching list of cache keys"
        cacheKeysForPR=$(gh cache list --ref "$BRANCH" --limit 100 --json id --jq '.[].id')

        ## Setting this to not fail the workflow while deleting cache keys.
        set +e
        echo "Deleting caches..."
        for cacheKey in $cacheKeysForPR
        do
            gh cache delete "$cacheKey"
        done
        echo "Done"
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        GH_REPO: ${{ github.repository }}
        BRANCH: refs/pull/${{ github.event.pull_request.number }}/merge
""".lstrip()


def read_yaml_file(file_path: str) -> dict[str, Any]:
    """Read and parse a YAML file.

    Args:
        file_path: Path to the YAML file

    Returns:
        Dict containing the parsed YAML content
    """
    yaml = YAML()
    yaml.preserve_quotes = True

    if os.path.exists(file_path):
        with open(file_path) as f:
            content = yaml.load(f) or {}
            return content
    return {}


def write_yaml_file(file_path: str, content: dict) -> bool:
    """Write content to a YAML file.

    The YAML formatting is hard-coded to match the format in .yamlfmt.yaml.

    Args:
        file_path: Path to the YAML file
        content: Content to write to the file

    Returns:
        True if the file was created, False if it already existed even if it was modified
    """
    # Configure YAML formatting to match .yamlfmt.yaml
    yaml = YAML()
    yaml.preserve_quotes = True
    # Basic formatter settings from .yamlfmt.yaml
    yaml.indent(mapping=2, sequence=4, offset=2)  # indentless_arrays: true
    yaml.width = 88
    yaml.map_indent = 2
    # Ensure compatibility with PyYAML
    yaml.default_flow_style = False
    file_created = not os.path.exists(file_path)

    # Write the content to the file
    logger.info(f"Writing changes to {file_path}")
    with open(file_path, "w") as f:
        yaml.dump(content, f)
    return file_created


def ensure_file_exists(file_path: str, default_content: str) -> bool:
    """Ensure a file exists with the specified content.

    If the file doesn't exist, create it with the default content.
    If the file exists, leave it unchanged.

    Args:
        file_path: Path to the file
        default_content: Default content for the file if it doesn't exist

    Returns:
        True we created the file, False if it already existed and was left unchanged
    """
    if not os.path.exists(file_path):
        logger.info(f"Creating {file_path} with default content")
        with open(file_path, "w") as f:
            f.write(default_content)
        return True
    return False


def add_hooks_to_repos(
    repos: list[PreCommitRepo],
    existing_repos: dict[str, PreCommitRepo],
    hooks_dict: dict[str, list[str | PreCommitHook]],
    hook_type: str = "",
) -> bool:
    """Add hooks to repositories.

    Args:
        repos: List of repositories
        existing_repos: Dictionary of existing repositories by URL
        hooks_dict: Dictionary of hooks to add
        hook_type: Type of hooks (for logging)

    Returns:
        True if the repos list was mutated, False otherwise
    """
    mutated = False
    for repo_url, hooks in hooks_dict.items():
        if repo_url in existing_repos:
            # Repository exists, check for missing hooks
            repo_config = existing_repos[repo_url]

            # Ensure hooks list exists
            if "hooks" not in repo_config:
                repo_config["hooks"] = []

            # Get existing hook IDs
            existing_hook_ids = {
                hook["id"] for hook in repo_config["hooks"] if "id" in hook
            }

            # Add missing hooks
            for hook in hooks:
                # Handle both string hook IDs and dictionaries with id and args
                hook_config: PreCommitHook
                if isinstance(hook, str):
                    hook_id = hook
                    hook_config = {"id": hook_id}
                else:
                    hook_id = hook["id"]
                    hook_config = hook.copy()

                if hook_id not in existing_hook_ids:
                    mutated = True
                    type_prefix = f"{hook_type} " if hook_type else ""
                    logger.info(
                        f"Adding {type_prefix}hook {hook_id} to repository {repo_url}"
                    )
                    repo_config["hooks"].append(hook_config)
        else:
            mutated = True
            # Repository doesn't exist, add it with default version and hooks
            type_prefix = f"{hook_type} " if hook_type else ""
            logger.info(f"Adding repository {repo_url} with {type_prefix}hooks")

            # Convert hooks to proper format
            hook_configs = []
            for hook in hooks:
                if isinstance(hook, str):
                    hook_configs.append(PreCommitHook(id=hook))
                else:
                    hook_configs.append(hook.copy())

            new_repo = PreCommitRepo(
                repo=repo_url,
                rev=DEFAULT_REPO_VERSIONS.get(repo_url, "main"),
                hooks=hook_configs,
            )
            repos.append(new_repo)
            existing_repos[repo_url] = new_repo

    return mutated


def ensure_pre_commit_config(config_path: str) -> bool:
    """Ensure the pre-commit config file exists and has the required hooks.

    Args:
        config_path: Path to the pre-commit config file

    Returns:
        True if the file was created, False if it already existed even if it was modified
    """
    try:
        file_exists = os.path.exists(config_path)
        # Read the current config
        config = read_yaml_file(config_path)

        # Initialise config if it doesn't exist
        if not config:
            config = {
                "repos": [],
            }

        # Ensure repos exists
        if "repos" not in config:
            config["repos"] = []

        # Get the current repositories
        repos = config["repos"]

        # Track existing repositories by URL
        existing_repos = {repo["repo"]: repo for repo in repos if "repo" in repo}

        # Track mutations
        mutated = False

        # Add missing repositories and hooks from DEFAULT_HOOKS
        mutated = add_hooks_to_repos(repos, existing_repos, DEFAULT_HOOKS) or mutated

        # Add GitHub Actions hooks if .github/workflows directory exists
        if os.path.exists(".github/workflows"):
            mutated = (
                add_hooks_to_repos(
                    repos, existing_repos, GITHUB_ACTIONS_HOOKS, "GitHub Actions"
                )
                or mutated
            )

        # Add Renovate hooks if renovate.json file exists
        if os.path.exists("renovate.json"):
            mutated = (
                add_hooks_to_repos(repos, existing_repos, RENOVATE_HOOKS, "Renovate")
                or mutated
            )

        # Write the updated config
        if mutated:
            return write_yaml_file(config_path, config)
        return not file_exists

    except Exception as e:
        raise Exception("Error ensuring pre-commit config") from e


def main() -> None:
    """Ensure that a baseline set of pre-commit hooks are enabled in the repository."""
    new_files = False

    try:
        # Ensure required files exist
        new_files = (
            ensure_file_exists(".editorconfig", DEFAULT_EDITORCONFIG) or new_files
        )
        new_files = ensure_file_exists(".yamlfmt.yaml", DEFAULT_YAMLFMT) or new_files
        new_files = ensure_file_exists(".gitignore", DEFAULT_GITIGNORE) or new_files

        if os.path.exists(".github/workflows"):
            new_files = (
                ensure_file_exists(
                    ".github/workflows/cleanup.yml", DEFAULT_ACTIONS_CACHE_CLEANUP
                )
                or new_files
            )

        # Ensure pre-commit config has required hooks
        new_files = ensure_pre_commit_config(".pre-commit-config.yaml") or new_files
    except Exception:
        error_logger.error("Error running init hooks", exc_info=True)
        sys.exit(2)

    if new_files:
        sys.exit(1)


if __name__ == "__main__":
    main()
