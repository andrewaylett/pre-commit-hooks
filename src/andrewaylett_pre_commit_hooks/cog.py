import os
import sys

from cogapp import Cog

from andrewaylett_pre_commit_hooks import error_logger, logger
from andrewaylett_pre_commit_hooks.common import handle_errors


@handle_errors
def find_cog_files() -> set[str] | bool:
    """Find files to process with cog.

    Looks for the first file that exists of `.cogfiles`, `README.md` or `README`.
    - If `.cogfiles` exists, use it as a list of files to check
    - If a README file exists, process just that file
    - If neither exists, return False

    Returns:
        A set of files to process, or False if an error occurred
    """
    # Check for .cogfiles first
    if os.path.exists(".cogfiles"):
        logger.info("Using .cogfiles to determine which files to process")
        with open(".cogfiles") as f:
            # Read the file list, strip whitespace, and filter out empty lines
            files = {line.strip() for line in f if line.strip()}
        if not files:
            error_logger.error("Error: .cogfiles exists but is empty")
            return False
        return files

    # Check for README.md next
    elif os.path.exists("README.md"):
        logger.info("Processing README.md")
        return {"README.md"}

    # Check for README last
    elif os.path.exists("README"):
        logger.info("Processing README")
        return {"README"}

    # If none of the files exist, return False
    else:
        error_logger.error("Error: Could not find .cogfiles, README.md, or README")
        return False


@handle_errors
def run_cog_on_files(files: set[str]) -> bool:
    """Run cog on the specified files.

    Returns True if all files were processed successfully, False otherwise.

    Note: Cog can only be run single-threaded, so files are processed sequentially.
    """
    if not files:
        logger.info("No files with cog markers found.")
        return True

    logger.info(f"Running cog on {len(files)} files...")
    success = True

    # Create a Cog instance with the appropriate options
    cog_instance = Cog()

    # Set options equivalent to command-line flags
    cog_instance.options.replace = True  # -r: replace in-place
    cog_instance.options.checksum = True  # -c: checksum
    cog_instance.options.verbosity = 3

    # Add imports to globals (equivalent to -p option)
    cog_instance.options.defines = {
        "subprocess": __import__("subprocess"),
        "sp": __import__("subprocess"),
        "re": __import__("re"),
        "os": __import__("os"),
        "sys": __import__("sys"),
        "pathlib": __import__("pathlib"),
        "pl": __import__("pathlib"),
        "cog": __import__("cogapp.cogapp"),
    }

    for file in files:
        try:
            # Process the content using process_string
            cog_instance.process_one_file(file)

        except Exception as e:
            error_logger.error(f"Error processing {file}: {e}")
            success = False

    return success


def main() -> None:
    """Find files with cog markers and run cog on them."""
    files = find_cog_files()
    success = run_cog_on_files(files)

    if not success:
        sys.exit(1)
