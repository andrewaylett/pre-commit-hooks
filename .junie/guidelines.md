# Development Guidelines for pre-commit-hooks

This document provides guidelines and instructions for developing and maintaining the pre-commit-hooks project.

## Build/Configuration Instructions

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) for package management

## Testing Information

### Running Tests

The project uses pytest for testing. To run all tests, formatting, linting, and typing:

```bash
uv run poe check
```

## Additional Development Information

### How Cog Works

The cog tool processes files with special markers:
- `[[[cog` marks the beginning of a code generation block
- `]]]` marks the end of the code generation block
- `[[[end]]]` marks the end of the generated output

The Python code between these markers is executed, and any output from `cog.outl()` or `cog.out()` is inserted into the file.

### Testing pre-commit hooks

The pre-commit documentation says:

Since the repo property of .pre-commit-config.yaml can refer to anything that git clone ... understands, it's often useful to point it at a local directory while developing hooks.

pre-commit try-repo streamlines this process by enabling a quick way to try out a repository. Here's how one might work interactively:

note: you may need to provide --commit-msg-filename when using this command with hook types prepare-commit-msg and commit-msg.

a commit is not necessary to try-repo on a local directory. pre-commit will clone any tracked uncommitted changes.

```
~/work/hook-repo $
# On a suitable branch ...

# ... make some changes

# In another terminal or tab

/tmp/testing/other-repo $ pre-commit try-repo ~/work/hook-repo foo --verbose --all-files
===============================================================================
Using config:
===============================================================================
repos:
-   repo: ../hook-repo
    rev: 84f01ac09fcd8610824f9626a590b83cfae9bcbd
    hooks:
    -   id: foo
===============================================================================
[INFO] Initializing environment for ../hook-repo.
Foo......................................................................Passed
- hook id: foo
- duration: 0.02s

Hello from foo hook!
```
