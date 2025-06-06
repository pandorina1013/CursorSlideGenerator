#!/usr/bin/env python3
"""CLI script for validating Marp presentations."""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from marp_slide_generator.tests.slide_validator import run_validation


def main():
    parser = argparse.ArgumentParser(description="Validate Marp slide presentations")
    parser.add_argument(
        "presentation_dir",
        help="Path to the presentation directory to validate"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code if warnings are found"
    )
    
    args = parser.parse_args()
    
    # Run validation
    error_count, warning_count = run_validation(args.presentation_dir)
    
    # Determine exit code
    if error_count > 0:
        sys.exit(1)
    elif args.strict and warning_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main() 