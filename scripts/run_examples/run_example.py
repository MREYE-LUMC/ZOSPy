# /// script
# dependencies = [
#   "ipykernel",
#   "nbconvert",
# ]
# ///

"""Run a ZOSPy example.

This script is used to run a single ZOSPy example. It is called by `run_all_examples.py` or `run_single_example.py`;
these scripts make sure the notebook is run in a separate environment with the required dependencies.
The script reads a Jupyter notebook, changes the connection mode from extension to standalone
(unless configured to do so), runs the notebook, and saves the output.
"""

from __future__ import annotations

import argparse
import re
import sys
import traceback
from pathlib import Path
from typing import Literal

import nbformat
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

ConnectionMode = Literal["standalone", "extension"]


def change_connection_mode(
    notebook: nbformat.NotebookNode,
    from_mode: ConnectionMode = "standalone",
    to_mode: ConnectionMode = "extension",
) -> str | None:
    regex_mode = re.compile(rf'zos\.connect\(\s*(?:mode\s*=\s*)?"{from_mode}"\s*\)')

    for cell in notebook.cells:
        if cell.cell_type == "code" and regex_mode.search(cell.source):
            mode = regex_mode.search(cell.source).group(0)
            cell.source = regex_mode.sub(f'zos.connect("{to_mode}")', cell.source)
            return mode

    return None


def process_notebook(
    notebook_path: Path,
    output_folder: Path | None = None,
    *,
    keep_extension_mode: bool = False,
) -> bool:
    nb = nbformat.read(notebook_path, as_version=4)

    # Change the connection mode to 'standalone' to run the notebook
    old_connection_mode = change_connection_mode(nb, "extension", "standalone") if not keep_extension_mode else False

    # Run the notebook
    ep = ExecutePreprocessor(kernel_name="python3")
    try:
        ep.preprocess(nb, {"metadata": {"path": notebook_path.parent}})
    except CellExecutionError:
        print(f"Error executing {notebook_path}: {traceback.format_exc()}")
        return False

    # Reverse the connection mode change
    if old_connection_mode:
        change_connection_mode(nb, "standalone", "extension")

    # Save the output
    output_path = notebook_path if output_folder is None else output_folder / notebook_path.name
    print(f"Saving output to {output_path}")
    nbformat.write(nb, output_path)

    return True


def main(args: argparse.Namespace) -> int:
    example_path: Path = Path(args.example).resolve(strict=False)
    output_path: Path = args.output or example_path

    if not example_path.exists():
        print(f"Directory {example_path} does not exist")
        return -1

    if not example_path.is_dir():
        print(f"Notebook {example_path} is not a directory. Please provide a directory.")
        return -1

    if not output_path.exists():
        print(f"Creating output directory at {args.output}")
        try:
            output_path.mkdir()
        except FileNotFoundError:
            print(f"Error creating output directory: {traceback.format_exc()}")
            return -1

    exitcode = 0

    for notebook in example_path.glob("*.ipynb"):
        print(f"Processing {notebook}...")
        success = process_notebook(notebook, args.output, keep_extension_mode=args.keep_extension_mode)

        if not success:
            print(f"Failed to process {notebook}.")
            exitcode += 1

    return exitcode


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Run a single example")
    parser.add_argument("example", type=Path, help="Path to the example directory")
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to save the output to. Defaults to the input example directory.",
    )
    parser.add_argument(
        "--keep-extension-mode",
        action="store_true",
        help="Keep the extension connection mode after running the notebook",
    )

    args = parser.parse_args()

    sys.exit(main(args))
