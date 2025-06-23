# Development Guidelines for pre-commit-hooks

This document provides guidelines and instructions for developing and maintaining the pre-commit-hooks project.

## Build/Configuration Instructions

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) for package management

### Project Structure

- `src/pre_commit_hooks/`: Source code for the pre-commit hooks
  - `cog.py`: Implementation of the cog pre-commit hook
- `tests/`: Test files
- `.pre-commit-hooks.yaml`: Configuration for the pre-commit hooks

## Testing Information

### Running Tests

The project uses pytest for testing. To run all tests:

```bash
uv run pytest
```

To run a specific test file:

```bash
uv run pytest tests/test_file.py
```

To run tests with verbose output:

```bash
uv run pytest -v
```

### Adding New Tests

1. Create a new test file in the `tests/` directory with a name starting with `test_`.
2. Import pytest and the modules you want to test.
3. Write test functions with names starting with `test_`.

#### Example Test with Cog

Here's an example of a test that uses cog to generate code:

```python
"""Example test file to demonstrate testing with cog."""

import pytest

def example_function_with_cog():
    """Example function with cog-generated content."""
    # [[[cog
    # import cog
    # numbers = [1, 2, 3, 4, 5]
    # cog.outl("    result = sum([" + ", ".join(str(n) for n in numbers) + "])")
    # ]]]
    result = sum([1, 2, 3, 4, 5])
    # [[[end]]]
    return result

def test_example_function_with_cog():
    """Test that the example function returns the expected value."""
    result = example_function_with_cog()
    assert result == 15
```

## Additional Development Information

### How Cog Works

The cog tool processes files with special markers:
- `[[[cog` marks the beginning of a code generation block
- `]]]` marks the end of the code generation block
- `[[[end]]]` marks the end of the generated output

The Python code between these markers is executed, and any output from `cog.outl()` or `cog.out()` is inserted into the file.

### Ripgrep Dependency

The hook uses ripgrep (`rg`) to efficiently find files containing cog markers. Make sure ripgrep is installed on your system.

### Error Handling

The hook is designed to:
1. Find all files with cog markers
2. Run cog on each file
3. Exit with a non-zero status if any file fails to process

### Python Version

The project requires Python 3.13 or higher, as specified in the `pyproject.toml` file.

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
