import os
import subprocess
import sys

from andrewaylett_pre_commit_hooks import error_logger, logger
from andrewaylett_pre_commit_hooks.common import handle_errors


@handle_errors
def run_uv_command(args: list[str], use_exec: bool = False) -> bool:
    """Run a command using uv run.

    Args:
        args: Arguments to pass to uv run
        use_exec: If True, use os.execvp to replace the current process with uv

    Returns:
        True if the command succeeded, False otherwise
        Note: If use_exec is True, this function will not return if successful
    """
    if not args:
        error_logger.error("Error: No command specified for uv run")
        return False

    command = ["uv", "run", *args]
    logger.info(f"Running: {' '.join(command)}")

    if use_exec:
        # Replace the current process with uv
        # This will not return if successful
        os.execvp("uv", command)
        # This line will only be reached in tests when os.execvp is mocked
        # noinspection PyUnreachableCode
        return True
    else:
        # Run the command and capture output
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )

        # Print the output
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)

        # Check if the command succeeded
        if result.returncode != 0:
            error_logger.error(f"Command failed with exit code {result.returncode}")
            return False

        return True


def main() -> None:
    """Execute a project command using uv run."""
    # Get arguments from command line, skipping the script name
    args = sys.argv[1:]

    # Use exec by default in the main function
    # This will replace the current process with uv
    success = run_uv_command(args, use_exec=True)

    # This will only be reached if use_exec=True fails
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
