# Runs Cog as a pre-commit hook

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
```""")
]]] -->
```yaml
repos:
- repo: https://github.com/andrewaylett/pre-commit-hooks
  rev: v0.1.0
  hooks:
    - id: cog
```
<!-- [[[end]]] -->

## Development

### Running Tests

This project uses pytest for testing. To run the tests:

```bash
uv run pytest
```

The test suite includes:
- Tests for the pre-commit hook functionality
- Tests for cog-generated content
