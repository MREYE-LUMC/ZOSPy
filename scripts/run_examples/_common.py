from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

EXECUTOR_PYTHON_VERSION: str = "3.12"
SCRIPT_DIR = Path(__file__).parent.resolve(strict=True)


def _dependencies_args(dependencies: set[str]) -> list[str]:
    result = []

    for dep in dependencies:
        result.extend(["--with", dep])

    return result


def _quote(s: Any) -> str:
    return f'"{s!s}"'


def get_dependencies_from_requirements(requirements: Path) -> list[str]:
    with requirements.open("r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def run_example_with_uv(
    example_path: Path,
    output_path: Path | None = None,
    requirements: Path | None = None,
    *,
    editable_zospy_location: Path | None = None,
    keep_extension_mode: bool = False,
) -> bool:
    # Build dependencies string
    dependencies = {"ipykernel"}

    if requirements is not None:
        dependencies.update(get_dependencies_from_requirements(requirements))

    # Use the editable zospy location if provided, otherwise use the required zospy version
    required_zospy = next((dep for dep in dependencies if dep.startswith("zospy")), None)
    dependencies.discard(required_zospy)
    dependencies_arguments = _dependencies_args(dependencies)

    if editable_zospy_location is not None:
        dependencies_arguments.extend(["--with-editable", editable_zospy_location.as_posix()])
    elif required_zospy is not None:
        dependencies_arguments.extend(["--with", required_zospy])
    else:
        dependencies_arguments.extend(["--with", "zospy"])

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
        *dependencies_arguments,
        "--no-project",  # Do not run in the project environment
        str(SCRIPT_DIR / "run_example.py"),
        ".",  # The command is run in the example directory
        *parameters,
    ]

    print(f"Running example {example_path} with command: {' '.join(command)}")

    return subprocess.run(command, check=False, cwd=example_path).returncode == 0


def process_example(
    example_path: Path,
    output_path: Path | None = None,
    editable_zospy_location: str | None = None,
    *,
    keep_extension_mode: bool = False,
) -> bool:
    """Run a single example and save the output."""
    requirements = example_path / "requirements.txt" if (example_path / "requirements.txt").exists() else None

    # Run the example
    return run_example_with_uv(
        example_path,
        output_path,
        requirements,
        editable_zospy_location=editable_zospy_location,
        keep_extension_mode=keep_extension_mode,
    )
