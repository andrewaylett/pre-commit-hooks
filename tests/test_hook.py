"""Tests for the cog pre-commit hook."""

import os
import tempfile
from pathlib import Path

from pre_commit_hooks.cog import find_cog_files, main, run_cog_on_files


def create_test_file_with_cog(content, temp_dir, filename="test_file.py"):
    """Create a test file with cog markers in the given temporary directory."""
    file_path = Path(temp_dir) / filename
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_find_cog_files():
    """Test that find_cog_files correctly identifies files with cog markers."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file with cog markers
        cog_content = """
def example():
    # [[[cog
    # import cog
    # cog.outl("    print('Generated')")
    # ]]]
    # Content will be generated here
    # [[[end]]]
    pass
"""
        create_test_file_with_cog(cog_content, temp_dir, "with_cog.py")

        # Create a file without cog markers
        no_cog_content = """
def example():
    print("No cog markers here")
    pass
"""
        create_test_file_with_cog(no_cog_content, temp_dir, "without_cog.py")

        # Change to the temporary directory
        original_dir = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Find cog files
            files = find_cog_files()

            # Check that only the file with cog markers is found
            assert len(files) == 1
            assert Path(files[0]).name == "with_cog.py"
        finally:
            # Change back to the original directory
            os.chdir(original_dir)


def test_run_cog_on_files():
    """Test that run_cog_on_files correctly processes files with cog markers."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file with cog markers
        cog_content = """
def example():
    # [[[cog
    # import cog
    # cog.outl("    print('Generated')")
    # ]]]
    # Content will be generated here
    # [[[end]]]
    pass
"""
        cog_file = create_test_file_with_cog(cog_content, temp_dir, "with_cog.py")

        # Run cog on the file
        success = run_cog_on_files([str(cog_file)])

        # Check that cog ran successfully
        assert success is True

        # Read the processed file
        with open(cog_file) as f:
            processed_content = f.read()

        # Check that the cog-generated content is present
        assert "print('Generated')" in processed_content


def test_main_with_temp_files():
    """Test the main function with temporary files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file with cog markers
        cog_content = """
def example():
    # [[[cog
    # import cog
    # cog.outl("    print('Generated')")
    # ]]]
    # Content will be generated here
    # [[[end]]]
    pass
"""
        cog_file = create_test_file_with_cog(cog_content, temp_dir, "with_cog.py")

        # Change to the temporary directory
        original_dir = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Run the main function
            main()

            # Read the processed file
            with open(cog_file) as f:
                processed_content = f.read()

            # Check that the cog-generated content is present
            assert "print('Generated')" in processed_content
        finally:
            # Change back to the original directory
            os.chdir(original_dir)
