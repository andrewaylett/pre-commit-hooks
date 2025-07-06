import os
import sys

from ruamel.yaml import YAML

from andrewaylett_pre_commit_hooks import error_logger, logger

# Default versions for repositories
DEFAULT_REPO_VERSIONS = {
    "https://github.com/pre-commit/pre-commit-hooks": "v5.0.0",
    "https://github.com/google/yamlfmt": "v0.17.2",
    "https://github.com/rhysd/actionlint": "v1.7.7",
    "https://github.com/editorconfig-checker/editorconfig-checker.python": "3.2.1",
    "https://github.com/python-jsonschema/check-jsonschema": "0.33.2",
    "https://github.com/andrewaylett/pre-commit-hooks": "v0.3.0",
    "https://github.com/renovatebot/pre-commit-hooks": "41.23.0",
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
RENOVATE_HOOKS = {
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


def read_yaml_file(file_path: str) -> dict:
    """Read and parse a YAML file.

    Args:
        file_path: Path to the YAML file

    Returns:
        Dict containing the parsed YAML content
    """
    try:
        yaml = YAML()
        yaml.preserve_quotes = True

        if os.path.exists(file_path):
            with open(file_path) as f:
                content = yaml.load(f) or {}
                return content
        return {}
    except Exception as e:
        error_logger.error(f"Error reading YAML file {file_path}: {e}")
        return {}


def write_yaml_file(file_path: str, content: dict) -> bool:
    """Write content to a YAML file.

    Args:
        file_path: Path to the YAML file
        content: Content to write to the file

    Returns:
        True if successful, False otherwise
    """
    try:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.width = 88

        with open(file_path, "w") as f:
            yaml.dump(content, f)
        return True
    except Exception as e:
        error_logger.error(f"Error writing YAML file {file_path}: {e}")
        return False


def ensure_file_exists(file_path: str, default_content: str) -> bool:
    """Ensure a file exists with the specified content.

    If the file doesn't exist, create it with the default content.
    If the file exists, leave it unchanged.

    Args:
        file_path: Path to the file
        default_content: Default content for the file if it doesn't exist

    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            logger.info(f"Creating {file_path} with default content")
            with open(file_path, "w") as f:
                f.write(default_content)
        return True
    except Exception as e:
        error_logger.error(f"Error ensuring file {file_path} exists: {e}")
        return False


def add_hooks_to_repos(repos, existing_repos, hooks_dict, hook_type=""):
    """Add hooks to repositories.

    Args:
        repos: List of repositories
        existing_repos: Dictionary of existing repositories by URL
        hooks_dict: Dictionary of hooks to add
        hook_type: Type of hooks (for logging)

    Returns:
        None
    """
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
                if isinstance(hook, str):
                    hook_id = hook
                    hook_config = {"id": hook_id}
                else:
                    hook_id = hook["id"]
                    hook_config = hook.copy()

                if hook_id not in existing_hook_ids:
                    type_prefix = f"{hook_type} " if hook_type else ""
                    logger.info(
                        f"Adding {type_prefix}hook {hook_id} to repository {repo_url}"
                    )
                    repo_config["hooks"].append(hook_config)
        else:
            # Repository doesn't exist, add it with default version and hooks
            type_prefix = f"{hook_type} " if hook_type else ""
            logger.info(f"Adding repository {repo_url} with {type_prefix}hooks")

            # Convert hooks to proper format
            hook_configs = []
            for hook in hooks:
                if isinstance(hook, str):
                    hook_configs.append({"id": hook})
                else:
                    hook_configs.append(hook.copy())

            new_repo = {
                "repo": repo_url,
                "rev": DEFAULT_REPO_VERSIONS.get(repo_url, "main"),
                "hooks": hook_configs,
            }
            repos.append(new_repo)


def ensure_pre_commit_config(config_path: str) -> bool:
    """Ensure the pre-commit config file exists and has the required hooks.

    Args:
        config_path: Path to the pre-commit config file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the current config
        config = read_yaml_file(config_path)

        # Initialize config if it doesn't exist
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

        # Add missing repositories and hooks from DEFAULT_HOOKS
        add_hooks_to_repos(repos, existing_repos, DEFAULT_HOOKS)

        # Add GitHub Actions hooks if .github/workflows directory exists
        if os.path.exists(".github/workflows"):
            add_hooks_to_repos(
                repos, existing_repos, GITHUB_ACTIONS_HOOKS, "GitHub Actions"
            )

        # Add Renovate hooks if renovate.json file exists
        if os.path.exists("renovate.json"):
            add_hooks_to_repos(repos, existing_repos, RENOVATE_HOOKS, "Renovate")

        # Write the updated config
        return write_yaml_file(config_path, config)

    except Exception as e:
        error_logger.error(f"Error ensuring pre-commit config: {e}")
        return False


def main() -> None:
    """Ensure that a baseline set of pre-commit hooks are enabled in the repository."""
    success = True

    # Ensure required files exist
    success = ensure_file_exists(".editorconfig", DEFAULT_EDITORCONFIG) and success
    success = ensure_file_exists(".yamlfmt.yaml", DEFAULT_YAMLFMT) and success
    success = ensure_file_exists(".gitignore", DEFAULT_GITIGNORE) and success

    # Ensure pre-commit config has required hooks
    success = ensure_pre_commit_config(".pre-commit-config.yaml") and success

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
