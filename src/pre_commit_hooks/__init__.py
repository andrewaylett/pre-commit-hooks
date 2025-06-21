import shutil
import subprocess
import sys
from pathlib import Path


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

    for file in files:
        try:
            # Use subprocess to run cog on each file
            # -r: replace in-place
            # -c: checksum (only update if output would be different)
            # -p: add these imports to the globals
            cmd = [
                sys.executable,
                "-m",
                "cogapp",
                "-r",
                "-c",
                "-p",
                "import subprocess as sp, re, os, sys, pathlib as pl, cog",
                file,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)

            if result.returncode != 0:
                print(f"Error processing {file}: {result.stderr}", file=sys.stderr)
                success = False
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
