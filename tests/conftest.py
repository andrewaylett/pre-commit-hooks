"""Common fixtures for tests."""

import os
import tempfile

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "change_dir: mark test to change to the temporary directory"
    )


@pytest.fixture
def temp_dir(request):
    """Create a temporary directory for testing.

    Args:
        request: The pytest request object.

    Returns:
        str: The path to the temporary directory.

    Note:
        By default, this fixture does not change the current directory.
        To change the current directory, use the `change_dir` marker:

        @pytest.mark.change_dir
        def test_something(temp_dir):
            ...
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_dir = os.getcwd()

        # Check if the test is marked to change directory
        change_dir = request.node.get_closest_marker("change_dir") is not None

        if change_dir:
            os.chdir(temp_dir)

        yield temp_dir

        if change_dir:
            os.chdir(original_dir)
