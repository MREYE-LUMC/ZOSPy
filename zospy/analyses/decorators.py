"""Decorators for Pydantic dataclasses with default configurations."""

from __future__ import annotations

import dataclasses
from sys import version_info

import pydantic
from pydantic import ConfigDict, Field, PrivateAttr

if version_info <= (3, 11):
    from typing_extensions import dataclass_transform
else:
    from typing import dataclass_transform


__all__ = ("analysis_result", "analysis_settings")


def _default_config_dataclass(default_config: ConfigDict, cls=None, config: ConfigDict | None = None, **kwargs):
    """Pydantic dataclass with default configuration."""
    config = default_config if config is None else default_config.update(config)

    if cls is None:
        # Called with parentheses
        return pydantic.dataclasses.dataclass(config=config, **kwargs)

    return pydantic.dataclasses.dataclass(config=config, **kwargs)(cls)


@dataclass_transform(field_specifiers=(dataclasses.field, Field, PrivateAttr))
def analysis_result(cls=None, config: ConfigDict | None = None, **kwargs):
    """Pydantic dataclass with default configuration for analysis results."""
    default_config = ConfigDict(populate_by_name=True, ser_json_inf_nan="constants")
    return _default_config_dataclass(default_config, cls, config, **kwargs)


@dataclass_transform(field_specifiers=(dataclasses.field, Field, PrivateAttr))
def analysis_settings(cls=None, config: ConfigDict | None = None, **kwargs):
    """Pydantic dataclass with default configuration for analysis settings."""
    default_config = ConfigDict(validate_assignment=True)
    return _default_config_dataclass(default_config, cls, config, **kwargs)
