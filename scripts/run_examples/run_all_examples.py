"""Script to run all examples in a directory and save the output.

This script runs all examples using the `run_single_example.py` script and saves the output.
`uv` is used to run the examples in isolated environments, with only the required dependencies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Literal

from _common import process_example


def _handle_output_folder(output_folder: Path | None, example_folder: Path) -> Path:
    """Create the output folder if it does not exist and return the output path.

    Because only the output folder root is provided, the example name is appended to the output folder path.
    """
    if output_folder is not None:
        output_folder = output_folder.resolve(strict=False)
        if not output_folder.exists():
            print(f"Creating output directory at {output_folder}")
            output_folder.mkdir()

        return output_folder / example_folder.name

    return example_folder.resolve(strict=False)


def main(args: argparse.Namespace) -> Literal[1, 0]:
    directory: Path = args.example_directory

    if not directory.exists():
        print(f"Directory {directory} does not exist.")
        return 1

    if not directory.is_dir():
        print(f"{directory} is not a directory. Please provide a directory.")
        return 1

    subfolders = [f for f in directory.iterdir() if f.is_dir()]

    if len(subfolders) == 0:
        print(f"No subdirectories found in {directory}, exiting.")
        return 1

    success: dict[Path, bool] = {}

    for subfolder in subfolders:
        if len(list(subfolder.glob("*.ipynb"))) == 0:
            print(f"No notebooks found in {subfolder}, skipping.")
            continue

        output_folder = _handle_output_folder(args.output, subfolder)

        print(f"Processing example {subfolder}")
        zospy_location = args.zospy_location.resolve(strict=False) if args.zospy_location is not None else None
        success[subfolder] = process_example(
            subfolder,
            output_folder,
            editable_zospy_location=zospy_location,
            keep_extension_mode=args.keep_extension_mode,
        )

    print(
        "\n\n--- Results ---\n",
        *[f"{k}: {'Success' if v else 'Failure'}" for k, v in success.items()],
        sep="\n",
    )

    return 0 if all(success.values()) else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all examples in a directory and save the output.")
    (
        parser.add_argument(
            "example_directory",
            type=Path,
            help="Path to the directory containing the examples.",
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
