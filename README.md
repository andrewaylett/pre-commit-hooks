# Andrew's pre-commit hooks

Add this repo to your `.pre-commit-config.yaml`:

<!-- [[[cog
result = sp.run(
    ["git", "describe", "--tags"],
    capture_output=True,
    text=True,
    check=True
)
version = result.stdout.strip().split('-')[0]
cog.outl(f"""```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: {version}
  hooks:
    - id: cog
    - id: init-hooks
```""")
]]] -->
```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.2.0
  hooks:
    - id: cog
    - id: init-hooks
```
<!-- [[[end]]] -->

## Available Hooks

### Cog

<!-- [[[cog
result = sp.run(
    ["git", "describe", "--tags"],
    capture_output=True,
    text=True,
    check=True
)
version = result.stdout.strip().split('-')[0]
cog.outl(f"""```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: {version}
  hooks:
    - id: cog
```""")
]]] -->
```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.2.0
  hooks:
    - id: cog
```
<!-- [[[end]]] -->

Runs [cog](https://github.com/nedbat/cog) against your `README.md`, `README`,
or if a file named `.cogfiles` exists, all files listed in that file.

The equivalent local incantation would be:

```bash
cog -r -c -p "import subprocess as sp, re, os, sys, pathlib as pl, cog" README.md
```

### Init hooks

<!-- [[[cog
result = sp.run(
    ["git", "describe", "--tags"],
    capture_output=True,
    text=True,
    check=True
)
version = result.stdout.strip().split('-')[0]
cog.outl(f"""```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: {version}
  hooks:
    - id: init-hooks
```""")
]]] -->
```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.2.0
  hooks:
    - id: init-hooks
```
<!-- [[[end]]] -->

Ensures that a baseline set of pre-commit hooks are enabled in the repository,
along with their support files.

* .pre-commit-config.yaml
  * trailing-whitespace
  * end-of-file-fixer
  * check-case-conflict
  * check-merge-conflict
  * check-yaml
  * check-toml
  * check-xml
  * check-added-large-files
  * forbid-submodules
  * mixed-line-ending
  * yamlfmt
  * actionlint
  * editorconfig-checker
  * check-github-workflows
  * check-renovate
  * init-hooks
* .editorconfig
  * Basic settings
* .yamlfmt.yaml
  * Basic settings
* .gitignore
  * Basic settings

If the files don't exist, they'll be created with sensible defaults.
If the files already exist, but are missing entries, the missing entries will be added.

## Development

### Running Tests

This project uses pytest for testing. To run the tests:

```bash
uv run pytest
```

The test suite includes:
- Tests for the pre-commit hook functionality
- Tests for cog-generated content
