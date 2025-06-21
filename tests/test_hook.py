"""Test for the cog pre-commit hook."""

from pre_commit_hooks import main


def test_main():
    """Test that the main function runs without errors."""
    # This is a simple test to ensure the main function can be called
    # In a real test, you would want to check the return value or side effects
    result = main()
    assert result is None or isinstance(result, int)
