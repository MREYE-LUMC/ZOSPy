"""Script to run an examples and save the output.

This script runs the specified example using the `run_single_example.py` script and saves the output.
`uv` is used to run the example in an isolated environment, with only the required dependencies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _common import process_example


def main(args: argparse.Namespace) -> int:
    example_directory: Path = args.example_directory.resolve()
    zospy_location = args.zospy_location.resolve(strict=False) if args.zospy_location is not None else None
    output_folder = args.output.resolve(strict=False) if args.output is not None else example_directory
    keep_extension_mode = args.keep_extension_mode

    if not example_directory.exists():
        print(
            f"Directory {example_directory} does not exist. Note: when run using Hatch, paths with backward slashes "
            "may not be found. Replace backward slashes with forward slashes in the path."
        )
        return 1

    if not example_directory.is_dir():
        print(f"{example_directory} is not a directory. Please provide a directory.")
        return 1

    success = process_example(
        example_directory,
        output_folder,
        editable_zospy_location=zospy_location,
        keep_extension_mode=keep_extension_mode,
    )

    if success:
        print(f"\n\nExample {example_directory} ran successfully.")
        return 0

    print(f"\n\nExample {example_directory} failed to run.")
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an example and save the output.")
    (
        parser.add_argument(
            "example_directory",
            type=Path,
            help="Path to the directory containing the example.",
        ),
    )
    parser.add_argument(
        "--zospy-location",
        type=Path,
        help="Path to the directory containing ZOSPy. If not provided, ZOSPy is installed from PyPI.",
        default=None,
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to save the output to. Defaults to the input example directory.",
        default=None,
    )
    parser.add_argument(
        "--keep-extension-mode",
        action="store_true",
        help="Do not change extension mode to standalone mode prior to running the notebook.",
    )

    args = parser.parse_args()

    sys.exit(main(args))
