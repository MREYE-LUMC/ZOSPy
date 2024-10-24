from __future__ import annotations

import pydantic
from pydantic import ConfigDict


def analysis_result(cls=None, config: ConfigDict | None = None, **kwargs):
    """Pydantic dataclass with default configuration for analysis results."""
    default_config = ConfigDict(populate_by_name=True)
    config = default_config if config is None else default_config.update(config)

    if cls is None:
        # Called with parentheses
        return pydantic.dataclasses.dataclass(config=config, **kwargs)

    return pydantic.dataclasses.dataclass(config=config, **kwargs)(cls)


def analysis_settings(cls=None, config: ConfigDict | None = None, **kwargs):
    """Pydantic dataclass with default configuration for analysis settings."""
    default_config = ConfigDict(validate_assignment=True)
    config = default_config if config is None else default_config.update(config)

    if cls is None:
        # Called with parentheses
        return pydantic.dataclasses.dataclass(config=config, **kwargs)

    return pydantic.dataclasses.dataclass(config=config, **kwargs)(cls)
