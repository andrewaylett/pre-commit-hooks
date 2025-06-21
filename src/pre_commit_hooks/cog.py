import sys
from pathlib import Path

import python_ripgrep
from cogapp import Cog


def find_cog_files() -> list[str]:
    """Find all files containing the '[[[cog' marker."""
    try:
        # Use python-ripgrep to find files with the [[[cog marker
        search_results = python_ripgrep.search([r"\[\[\[cog"], ["."])

        # Extract unique file paths from the search results
        # The search results are strings in the format "file_path:line_number:line_content"
        files = set()
        for result in search_results:
            # Extract the file path (everything before the first colon)
            file_path = result.split(":", 1)[0]
            files.add(file_path)

        # Convert to list and exclude our own implementation file
        current_file = Path(__file__).resolve()
        files = [f for f in files if Path(f).resolve() != current_file]

        return files
    except Exception as e:
        print(f"Error searching for cog files: {e}", file=sys.stderr)
        return []


def run_cog_on_files(files: list[str]) -> bool:
    """Run cog on the specified files.

    Returns True if all files were processed successfully, False otherwise.
    """
    if not files:
        print("No files with cog markers found.")
        return True

    print(f"Running cog on {len(files)} files...")
    success = True

    # Create a Cog instance with the appropriate options
    cog_instance = Cog()

    # Set options equivalent to command-line flags
    cog_instance.options.replaceCode = True  # -r: replace in-place
    cog_instance.options.checksum = True  # -c: checksum

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
            # Process the file using the Cog instance
            # Read the file content
            with open(file) as f:
                content = f.read()

            # Process the content using process_string
            processed_content = cog_instance.process_string(content)

            # Write the processed content back to the file
            with open(file, "w") as f:
                f.write(processed_content)
        except Exception as e:
            print(f"Error processing {file}: {e}", file=sys.stderr)
            success = False

    return success


def main() -> None:
    """Find files with cog markers and run cog on them."""
    files = find_cog_files()
    success = run_cog_on_files(files)

    if not success:
        sys.exit(1)
