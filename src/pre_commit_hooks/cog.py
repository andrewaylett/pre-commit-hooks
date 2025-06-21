import shutil
import subprocess
import sys
from pathlib import Path
from cogapp import Cog


def find_cog_files() -> list[str]:
    """Find all files containing the '[[[cog' marker."""
    try:
        # Check if ripgrep is available
        rg_path = shutil.which("rg")
        if not rg_path:
            print(
                "Error: ripgrep (rg) is not installed or not in PATH", file=sys.stderr
            )
            return []

        # Use ripgrep to find files with the [[[cog marker
        # Use --type-not=py to exclude Python files that might have the marker in comments
        # Then explicitly include Python files with the marker in a code context
        cmd = [rg_path, "-l", "\\[\\[\\[cog", "."]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if (
            result.returncode != 0 and result.returncode != 1
        ):  # rg returns 1 when no matches found
            print(f"Error running ripgrep: {result.stderr}", file=sys.stderr)
            return []

        # Extract file paths from results
        files = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        # Exclude our own implementation file
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
    cog_instance.options.checksum = True     # -c: checksum

    # Add imports to globals (equivalent to -p option)
    cog_instance.options.defines = {
        'subprocess': __import__('subprocess'),
        'sp': __import__('subprocess'),
        're': __import__('re'),
        'os': __import__('os'),
        'sys': __import__('sys'),
        'pathlib': __import__('pathlib'),
        'pl': __import__('pathlib'),
        'cog': __import__('cogapp.cogapp')
    }

    for file in files:
        try:
            # Process the file using the Cog instance
            # Read the file content
            with open(file, 'r') as f:
                content = f.read()

            # Process the content using process_string
            processed_content = cog_instance.process_string(content)

            # Write the processed content back to the file
            with open(file, 'w') as f:
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
