# Runs Cog as a pre-commit hook

Rather than adding a local pre-commit hook to each of your repositories:

```yaml
repos:
- repo: local
  hooks:
  - # https://github.com/nedbat/cog/issues/21#issuecomment-1919626992
    id: cog
    name: cog (regenerate files)
    language: python
    additional_dependencies:
    - cogapp
    entry: bash -c 'git grep -lzF "[[[""cog" | xargs -0 cog -r -c -p "import subprocess as sp, re, os, sys, pathlib as pl, cog" "$@"'
    pass_filenames: false
    always_run: true
```

We can use this repo to do the same thing:

```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  hooks:
    - id: cog
```

## Development

### Running Tests

This project uses pytest for testing. To run the tests:

1. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

2. Run the tests:
   ```bash
   uv run pytest
   ```

The test suite includes:
- Tests for the pre-commit hook functionality
- Tests for cog-generated content
