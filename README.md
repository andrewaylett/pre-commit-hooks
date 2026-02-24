# Andrew's pre-commit hooks

Add this repo to your `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.7.1
  hooks:
    - id: cog
    - id: init-hooks
```

## Available Hooks

### Cog

```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.7.1
  hooks:
    - id: cog
```

Runs [cog](https://github.com/nedbat/cog) against your `README.md`, `README`,
or if a file named `.cogfiles` exists, all files listed in that file.

The equivalent local incantation would be:

```bash
cog -r -c -p "import subprocess as sp, re, os, sys, pathlib as pl, cog" README.md
```

### UV

```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.7.1
  hooks:
    - id: uv-run
      name: Run pytest
      args:
        - pytest
        - --verbose
```

Executes a project command using `uv run`.

This is roughly equivalent to this local hook:

```yaml
- repo: local
  hooks:
  - id: uv-run
    name: Run pytest
    language: python
    entry: uv run pytest --verbose
    additional_dependencies:
    - "uv==0.10.5"
    pass_filenames: false
    always_run: true
```

The biggest difference is that pre-commit will cache the dedicated hook, while the local hook needs pre-commit
to download and use `virtualenv` and `uv` every time it's run.

### Init hooks

```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.7.1
  hooks:
    - id: init-hooks
```

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
  * editorconfig-checker
  * init-hooks
  * If `.github/workflows` directory exists:
    * actionlint
    * check-github-workflows
  * If `renovate.json` file exists:
    * check-renovate
* .editorconfig
  * Basic settings
* .yamlfmt.yaml
  * Basic settings
* .gitignore
  * Basic settings

If the files don't exist, they'll be created with sensible defaults.
If the files already exist, but are missing entries, the missing entries will be added.

## Development

### Dependencies

I highly recommend using [uv](https://docs.astral.sh/uv/) to manage your python environment for this tool.
You don't need to use uv directly if you only want to use the hooks from `pre-commit`,
and if you really want to develop the tool without touching `uv` then you _can_ run all the tests and lints using just `pre-commit`.

### Running Tests

This project uses [pytest](https://pytest.org) for testing,
[ruff](https://docs.astral.sh/ruff/) for linting and formatting,
and [pytype](https://google.github.io/pytype/) for typing.
To run them all using [poe](https://poethepoet.natn.io/):

```bash
uv run poe check
```

or using pre-commit:

```bash
uv run pre-commit run -a
```

or if you prefer:

```bash
pre-commit run -a
```
