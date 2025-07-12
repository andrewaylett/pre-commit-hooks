"""Common functionality for pre-commit hooks."""

import os
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from andrewaylett_pre_commit_hooks import error_logger, logger

# Type variable for generic function return type
T = TypeVar("T")


def handle_errors(func: Callable[..., T]) -> Callable[..., T | bool]:
    """Decorator to handle errors in functions.

    Args:
        func: The function to decorate

    Returns:
        A wrapped function that handles errors
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T | bool:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_logger.error(f"Error in {func.__name__}: {e}")
            return False

    return wrapper


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
