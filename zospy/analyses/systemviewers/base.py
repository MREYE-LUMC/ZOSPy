"""Base classes for system viewers.

System viewers are slightly different from other analyses: the analyses themselves are not configurable,
but there is a separate tool for each viewer. This module provides the base classes for interacting with these tools.
"""

from __future__ import annotations

import weakref
from abc import ABC, abstractmethod
from dataclasses import fields
from typing import TYPE_CHECKING, Annotated, Generic, Literal, Optional, get_args
from warnings import warn

import numpy as np
from pydantic.fields import Field, FieldInfo
from System import Array

from zospy.analyses.base import AnalysisData, AnalysisResult, AnalysisSettings, BaseAnalysisWrapper, OnComplete
from zospy.utils.pyutils import abspath

if TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path

    from zospy.api import _ZOSAPI
    from zospy.zpcore import OpticStudioSystem


__all__ = ("SystemViewerWrapper", "ImageSize")


class SystemViewerWrapper(BaseAnalysisWrapper[Optional[np.ndarray], AnalysisSettings], ABC, Generic[AnalysisSettings]):
    """Base class for SystemViewer analyses."""

    ALLOWED_IMAGE_EXTENSIONS: tuple[str, ...] = ("bmp", "jpeg", "png")

    def __init__(self, settings_kws: dict[str, any]):
        super().__init__(settings_kws=settings_kws)

        self._image_output_file = None

    def __init_subclass__(cls, **kwargs):
        """Determine the settings type of the viewer."""
        if cls._settings_type is AnalysisSettings:
            if hasattr(cls, "__orig_bases__"):
                base = cls.__orig_bases__[0]
                cls._settings_type: type[AnalysisSettings] = get_args(base)[0]
            else:
                cls._settings_type = type(None)  # TODO: Replace with NoneType when dropping support for Python 3.9

        super().__init_subclass__(**kwargs)

    @property
    def image_output_file(self) -> str | Path | None:
        """Path to the image output file."""
        return self._image_output_file

    def _warn_ignored_settings(self) -> None:
        """Check if unsupported parameters are specified and warn the user.

        For OpticStudio versions below 24R1, compare the values of a dictionary with the default values of a function,
        and warn if any are different.
        """
        changed_parameters = []

        for field in fields(type(self.settings)):
            default = field.default.default if isinstance(field.default, FieldInfo) else field.default

            if getattr(self.settings, field.name) != default:
                changed_parameters.append(field.name)

        if len(changed_parameters) > 0:
            warn(
                f"Some parameters were specified but ignored, because viewer exports are only supported from OpticStudio"
                f"24R1: {', '.join(changed_parameters)}"
            )

    def _validate_path(self, path: PathLike | str) -> str:
        str_path = abspath(path, check_directory_only=True)

        if str_path.split(".")[-1] in self.ALLOWED_IMAGE_EXTENSIONS:
            return str_path

        raise ValueError(f"Image file must have one of the following extensions: {self.ALLOWED_IMAGE_EXTENSIONS}")

    def _validate_wavelength(self, wavelength: int | str) -> int:
        if isinstance(wavelength, str):
            if wavelength == "All":
                return -1

            raise ValueError("wavelength must be an integer or 'All'.")

        if wavelength < -1 or wavelength == 0 or wavelength > self.oss.SystemData.Wavelengths.NumberOfWavelengths:
            raise ValueError("wavelength must be -1 or between 1 and the number of wavelengths.")

        if not isinstance(wavelength, int):
            raise TypeError("wavelength must be an integer or 'All'.")

        return wavelength

    def _validate_field(self, field: int | str) -> int:
        if isinstance(field, str):
            if field == "All":
                return -1

            raise ValueError("field must be an integer or 'All'.")

        if field < -1 or field == 0 or field > self.oss.SystemData.Fields.NumberOfFields:
            raise ValueError("field must be -1 or between 1 and the number of fields.")

        if not isinstance(field, int):
            raise TypeError("field must be an integer or 'All'.")

        return field

    def _validate_end_surface(self, start_surface, end_surface: int):
        if end_surface != -1 and end_surface <= start_surface or end_surface > self.oss.LDE.NumberOfSurfaces - 1:
            raise ValueError(
                "end_surface must be -1 or greater than start_surface and less than the number of surfaces."
            )

        if end_surface == -1:
            return self.oss.LDE.NumberOfSurfaces - 1

        return end_surface

    def _close_current_tool(self) -> None:
        """Close the current tool in OpticStudio."""
        if self.oss.Tools.CurrentTool is not None:
            self.oss.Tools.CurrentTool.Close()

    @staticmethod
    def _get_image_data(image_data: _ZOSAPI.Tools.Layouts.IImageExportData | None) -> np.ndarray | None:
        if image_data is None:
            return image_data

        image_size = image_data.Width * image_data.Height

        # In-place updating arrays works only with dotnet arrays
        r_values = Array[int](image_size)  # [0] * image_size
        g_values = Array[int](image_size)  # [0] * image_size
        b_values = Array[int](image_size)  # [0] * image_size

        image_data.FillValues(image_data.Width * image_data.Height, r_values, g_values, b_values)

        return np.stack((r_values, g_values, b_values), axis=-1).reshape(image_data.Height, image_data.Width, 3)

    @abstractmethod
    def configure_layout_tool(
        self,
    ) -> (
        _ZOSAPI.Tools.Layouts.ICrossSectionExport
        | _ZOSAPI.Tools.Layouts.I3DViewerExport
        | _ZOSAPI.Tools.Layouts.IShadedModelExport
        | _ZOSAPI.Tools.Layouts.INSC3DLayoutExport
        | _ZOSAPI.Tools.Layouts.INSCShadedModelExport
    ):
        """Configure the layout tool for the analysis."""

    def run_analysis(self) -> np.ndarray | None:
        """Run the layout tool."""
        layout_tool = self.configure_layout_tool()

        if self.image_output_file is not None:
            layout_tool.SaveImageAsFile = True
            layout_tool.OutputFileName = self.image_output_file
        else:
            layout_tool.SaveImageAsFile = False

        layout_tool.RunAndWaitForCompletion()

        if not layout_tool.Succeeded:
            raise RuntimeError("The system viewer export tool failed to run.")

        image_data = self._get_image_data(layout_tool.ImageExportData) if self.image_output_file is None else None

        layout_tool.Close()

        return image_data

    def run(
        self,
        oss: OpticStudioSystem,
        image_output_file: str | Path | None = None,
        oncomplete: OnComplete | Literal["Close", "Release", "Sustain"] = "Close",
    ) -> AnalysisData:
        """Run the analysis.

        Parameters
        ----------
        **kwargs
        """
        if image_output_file is not None:
            self._image_output_file = self._validate_path(image_output_file)

        self._oss = weakref.proxy(oss)
        self._create_analysis(settings_first=False)

        image_data = None

        if self.oss.ZOS.version >= (24, 1, 0):
            self._close_current_tool()
            image_data = self.run_analysis()
        else:
            self._warn_ignored_settings()

        result = AnalysisResult(
            image_data,
            settings=self.settings,
            metadata=self.analysis.metadata,
            header=self.analysis.header_data,
            messages=self.analysis.messages,
        )

        self._complete(OnComplete(oncomplete))

        return result


_UInt = Annotated[int, Field(gt=0)]
ImageSize = tuple[_UInt, _UInt]
