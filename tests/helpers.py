from __future__ import annotations

from dataclasses import fields, is_dataclass

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal


def assert_dataclass_equal(
    a, b, *, return_bool: bool = False, tolerance: float = 1e-5, ignore_fields: list[str] | None = None
) -> None | bool:
    if not is_dataclass(a) and not is_dataclass(b):
        raise ValueError("Both result and expected must be dataclasses")

    fields_a, fields_b = fields(a), fields(b)

    missing_fields = {f.name for f in fields_a}.symmetric_difference(f.name for f in fields_b)
    differences = {}

    ignore_fields = ignore_fields or []

    for f in fields(a):
        if f.name in missing_fields or f.name in ignore_fields:
            continue

        value_a = getattr(a, f.name)
        value_b = getattr(b, f.name)

        if isinstance(value_a, pd.DataFrame) and isinstance(value_b, pd.DataFrame):
            try:
                assert_frame_equal(value_a, value_b, rtol=tolerance)
            except AssertionError:
                differences[f.name] = (value_a, value_b)
        elif isinstance(value_a, np.ndarray) and isinstance(value_b, np.ndarray):
            if not np.allclose(value_a, value_b, rtol=tolerance):
                differences[f.name] = (value_a, value_b)
        elif is_dataclass(value_a) and is_dataclass(value_b):
            if not assert_dataclass_equal(value_a, value_b, return_bool=True):
                differences[f.name] = (value_a, value_b)
        elif isinstance(value_a, (list, tuple)) and isinstance(value_b, (list, tuple)):
            if is_dataclass(value_a[0]):
                for i, (item_a, item_b) in enumerate(zip(value_a, value_b)):
                    if not assert_dataclass_equal(item_a, item_b, return_bool=True):
                        differences[f"{f.name}[{i}]"] = (item_a, item_b)
        elif value_a != value_b:
            differences[f.name] = (value_a, value_b)

    if missing_fields or differences:
        if return_bool:
            return False

        missing_fields_message = (
            f"Fields: {''.join(missing_fields)} are not present in both dataclasses." if (missing_fields) else ""
        )
        differences_message = f"The following fields are unequal: {differences}" if differences else ""
        message = (
            f"{missing_fields_message} {differences_message}"
            if missing_fields_message and differences_message
            else (missing_fields_message or differences_message)
        )

        raise AssertionError(message)

    if return_bool:
        return True

    return None
