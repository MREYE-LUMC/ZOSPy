"""Zernike Coefficients vs. Field analysis."""

from __future__ import annotations

from typing import Annotated, Literal, get_args

import numpy as np
import pandas as pd
from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.transformers import ZospyTransformer
from zospy.analyses.parsers.types import ZOSAPIConstant  # noqa: TC001
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling

__all__ = ("ZernikeCoefficientsVsField", "ZernikeCoefficientsVsFieldSettings")


class ZernikeCoefficientsVsFieldTransformer(ZospyTransformer):
    """Lark Transformer for the Zernike Coefficients vs. Field analysis."""

    def start(self, args):  # noqa: PLR6301
        """Transform the root of the parse tree."""
        return args[0]

    def zernike_vs_field_table(self, args):  # noqa: PLR6301
        """Transform the Zernike vs. Field table to a DataFrame."""
        header, rows = args[0]

        if header[0] != "Field:":
            raise ValueError("Expected 'Field' column at the start of the table header.")

        values = np.array(rows, dtype=float)
        index = values[:, 0]  # First column is the index (Field coordinate)
        data = values[:, 1:]  # Remaining columns are the data

        return pd.DataFrame(
            data=data,
            index=pd.Index(index, name="Field"),
            columns=header[1:],  # Exclude 'Field:' from columns
        )


FieldScanDirection = Literal["+x", "-x", "+y", "-y"]


@analysis_settings
class ZernikeCoefficientsVsFieldSettings:
    """Settings for the Zernike vs. Field analysis.

    For an in depth explanation of the parameters, see the OpticStudio user manual.

    Attributes
    ----------
    coefficients : str
        The Zernike coefficients that are calculated, e.g. '1-6'. Defaults to '1-6'.
    wavelength : int
        The wavelength number that is to be used. Defaults to 1.
    coefficients_type : str | constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes
        Determines which Zernike coefficients are to be calculated. Should be one of ['Fringe', 'Standard', 'Annular'].
    Defaults to 'Fringe'.
    field_scan : str | constants.Analysis.Settings.Aberrations.FieldScanDirections
        The field scan direction. Should be one of ['+y', '-y', '+x', '-x']. Defaults to '+y'.
    field_density : int
        The field density. Defaults to 20.
    sampling : str | constants.Analysis.SampleSizes
        The sampling, formatted as '...x...' where the dots represent numbers (e.g. '64x64'). Defaults to '64x64'.
    obscuration : float
        The obscuration factor. Is only used when coefficient_type == 'Annular'. Defaults to 0.5.
    minimum_plot_scale : float
        The minimum plot scale. When 0, OpticStudio will choose the value. Defaults to 0.
    maximum_plot_scale : float
        The maximum plot scale. When 0, OpticStudio will choose the value. Defaults to 0.
    """

    coefficients: Annotated[str, Field(pattern=r"^\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*$")] = "1-8"
    wavelength: Annotated[int, Field(gt=0)] = 1
    coefficients_type: ZOSAPIConstant("Analysis.Settings.Aberrations.ZernikeCoefficientTypes") = "Standard"
    field_scan: ZOSAPIConstant("Analysis.Settings.Aberrations.FieldScanDirections") | FieldScanDirection = "+y"
    field_density: int = 20
    sampling: str = "64x64"
    obscuration: float = 0.5
    minimum_plot_scale: float = 0
    maximum_plot_scale: float = 0


class ZernikeCoefficientsVsField(
    BaseAnalysisWrapper[pd.DataFrame, ZernikeCoefficientsVsFieldSettings],
    analysis_type="ZernikeCoefficientsVsField",
    needs_text_output_file=True,
):
    """Zernike Coefficients vs. Field analysis."""

    def __init__(
        self,
        *,
        coefficients: str = "1-8",
        wavelength: int = 1,
        coefficients_type: str | constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes = "Standard",
        field_scan: FieldScanDirection | constants.Analysis.Settings.Aberrations.FieldScanDirections = "+y",
        field_density: int = 20,
        sampling: str = "64x64",
        obscuration: float = 0.5,
        minimum_plot_scale: float = 0,
        maximum_plot_scale: float = 0,
    ):
        """Create a new Zernike Coefficients vs. Field analysis.

        See Also
        --------
        ZernikeCoefficientsVsFieldSettings : Settings for the Zernike Coefficients vs. Field analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> pd.DataFrame:
        """Run the Zernike Coefficients vs. Field analysis."""
        if self.settings.field_scan in get_args(FieldScanDirection):
            match self.settings.field_scan:
                case "+x":
                    self.settings.field_scan = constants.Analysis.Settings.Aberrations.FieldScanDirections.Plus_X
                case "-x":
                    self.settings.field_scan = constants.Analysis.Settings.Aberrations.FieldScanDirections.Minus_X
                case "+y":
                    self.settings.field_scan = constants.Analysis.Settings.Aberrations.FieldScanDirections.Plus_Y
                case "-y":
                    self.settings.field_scan = constants.Analysis.Settings.Aberrations.FieldScanDirections.Minus_Y

        self.analysis.Settings.Coefficients = self.settings.coefficients
        self.analysis.set_wavelength(self.settings.wavelength)
        self.analysis.Settings.ZernikeCoefficientType = constants.process_constant(
            constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes, self.settings.coefficients_type
        )
        self.analysis.Settings.FieldScanDirection = constants.process_constant(
            constants.Analysis.Settings.Aberrations.FieldScanDirections, self.settings.field_scan
        )
        self.analysis.Settings.FieldDensity = self.settings.field_density
        self.analysis.Settings.SampleSize = constants.process_constant(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.sampling)
        )

        if (
            self.analysis.Settings.ZernikeCoefficientType
            == constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes.Annular
        ):
            self.analysis.Settings.ObscurationFactor = self.settings.obscuration

        self.analysis.Settings.ScaleMinimum = self.settings.minimum_plot_scale
        self.analysis.Settings.ScaleMaximum = self.settings.maximum_plot_scale

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Parse output
        text_output = self.get_text_output()

        if "Insufficient Memory Available!" in text_output:
            raise RuntimeError("Zernike Coefficients vs. Field analysis failed due to insufficient memory.")

        result = self.parse_output("zernike_coefficients_vs_field", transformer=ZernikeCoefficientsVsFieldTransformer)

        if self.settings.field_scan in {
            constants.Analysis.Settings.Aberrations.FieldScanDirections.Minus_X,
            constants.Analysis.Settings.Aberrations.FieldScanDirections.Minus_Y,
        }:
            # OpticStudio output does not reflect negative field scans in the index
            result.index = -result.index

        return result
