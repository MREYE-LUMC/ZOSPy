"""
Script to run all examples in a directory and save the output.

This script runs all examples using the `run_single_example.py` script and saves the output.
`uv` is used to run the examples in isolated environments, with only the required dependencies.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Literal

EXECUTOR_PYTHON_VERSION: str = "3.12"
SCRIPT_DIR = Path(__file__).parent.resolve(strict=True)


def _dependencies_args(dependencies: list[str]) -> list[str]:
    result = []

    for dep in dependencies:
        result.extend(["--with", dep])

    return result


def _quote(s: Any) -> str:
    return f'"{s!s}"'


def run_example_with_uv(
    example_path: Path,
    output_path: Path | None = None,
    requirements: Path | None = None,
    *,
    keep_extension_mode: bool = False,
) -> bool:
    # Build dependencies string
    dependencies = _dependencies_args(["zospy", "ipykernel"])

    if requirements is not None:
        dependencies.extend(["--with-requirements", requirements.resolve().as_posix()])

    parameters = []

    if output_path is not None:
        parameters.extend(["--output", str(output_path)])

    if keep_extension_mode:
        parameters.append("--keep-extension-mode")

    # Use `uv` supplied by Hatch when running in a Hatch environment
    uv_exe = os.environ.get("HATCH_UV", "uv")

    command = [
        uv_exe,
        "run",
        "--python",
        EXECUTOR_PYTHON_VERSION,
        *dependencies,
        "--no-project",  # Do not run in the project environment
        str(SCRIPT_DIR / "run_single_example.py"),
        ".",  # The command is run in the example directory
        *parameters,
    ]

    print(f"Running example {example_path} with command: {' '.join(command)}")

    return subprocess.run(command, check=False, cwd=example_path).returncode == 0


def process_example(
    example_path: Path,
    output_path: Path | None = None,
    *,
    keep_extension_mode: bool = False,
) -> bool:
    """Run a single example and save the output."""
    requirements = example_path / "requirements.txt" if (example_path / "requirements.txt").exists() else None

    # Run the example
    return run_example_with_uv(example_path, output_path, requirements, keep_extension_mode=keep_extension_mode)


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
        success[subfolder] = process_example(subfolder, output_folder, keep_extension_mode=args.keep_extension_mode)

    print(
        "\n\n--- Results ---\n",
        *[f"{k}: {'Success' if v else 'Failure'}" for k, v in success.items()],
        sep="\n",
    )

    return 0 if all(success.values()) else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all examples in a directory and save the output.")
    parser.add_argument(
        "example_directory",
        type=Path,
        help="Path to the directory containing the examples.",
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
