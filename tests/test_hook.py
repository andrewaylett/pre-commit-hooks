#!/usr/bin/env python3
"""Test script for the cog pre-commit hook."""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from pre_commit_hooks import main

if __name__ == "__main__":
    print("Testing cog pre-commit hook...")
    main()
    print("Test completed.")
