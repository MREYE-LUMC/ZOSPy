"""Ray Fan (Ray Aberration) analysis."""

from __future__ import annotations

import re
from typing import Annotated, Literal

import numpy as np
import pandas as pd
from pandas import DataFrame
from pydantic import Field

from zospy.analyses.new.base import BaseAnalysisWrapper
from zospy.analyses.new.decorators import analysis_result, analysis_settings
from zospy.analyses.new.parsers.types import FieldNumber, UnitField, ValidatedDataFrame, WavelengthNumber
from zospy.api import config, constants

__all__ = ("RayFan", "RayFanSettings")

from zospy.utils.pyutils import atox


@analysis_result
class FanData:
    field_number: Annotated[int, Field(ge=0)]
    field_coordinate: UnitField[float]
    data: ValidatedDataFrame


@analysis_result
class RayFanResult:
    """Data for the Ray Fan analysis."""

    tangential: list[FanData]
    sagittal: list[FanData]


@analysis_settings
class RayFanSettings:
    """Settings for the Ray Fan analysis.

    Attributes
    ----------
    plot_scale : float
        Maximum vertical scale for the plots. When 0, automatic scaling is used. Defaults to 0.
    number_of_rays : int
        Number of rays traced on each side of the origin of the plot.
    field : str or int
        The field number that is to be used. Either 'All' or an integer specifying the field number. Defaults to 'All'.
    wavelength : str | int
        The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number.
        Defaults to 'All'.
    tangential : str | int
        The aberration component that is plotted for the tangential fan, either 'Aberration_Y' or
        'Aberration_X'. Defaults to 'Aberration_Y'.
    sagittal : str
        The aberration component that is plotted for the sagittal fan, either 'Aberration_X' or
        'Aberration_Y'. Defaults to 'Aberration_X'.
    surface : str | int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    use_dashes : bool
        Defines whether solid lines or dashes are used to differentiate curves. Defaults to `False`.
    vignetted_pupil : bool
        Defines whether the pupil axis is scaled to the unvignetted pupil or not. Defaults to `True`.
    check_apertures : bool
        Defines whether only rays that pass all surface apertures are drawn or not. Defaults to `True`.
    """

    plot_scale: float = Field(default=0, ge=0, description="Plot scale, use 0 for automatic scaling")
    number_of_rays: int = Field(default=10, ge=0, description="Number of rays to trace")
    field: FieldNumber = Field(default="All", description="Field number or 'All'")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number or 'All'")
    tangential: str = Field(default="Aberration_Y", description="Tangential aberration to plot")
    sagittal: str = Field(default="Aberration_X", description="Sagittal aberration to plot")
    surface: Literal["Image", "Object"] | Annotated[int, Field(ge=0)] = Field(
        default="Image", description="Surface " "to be analyzed"
    )
    use_dashes: bool = Field(default=False, description="Use dashed lines for the rays")
    vignetted_pupil: bool = Field(default=False, description="Scale the pupil axis to the unvignetted pupil")
    check_apertures: bool = Field(default=False, description="Only draw rays that pass all surface apertures")


class RayFan(BaseAnalysisWrapper[DataFrame | None, RayFanSettings]):
    """Ray Fan analysis."""

    TYPE = "RayFan"

    def __init__(
        self,
        *,
        plot_scale: float = 0,
        number_of_rays: int = 10,
        field: int | Literal["All"] = "All",
        wavelength: int | Literal["All"] = "All",
        tangential: str | constants.Analysis.Settings.Fans.TangentialAberrationComponent = "Aberration_Y",
        sagittal: str | constants.Analysis.Settings.Fans.SagittalAberrationComponent = "Aberration_X",
        surface: str | int = "Image",
        use_dashes: bool = False,
        vignetted_pupil: bool = True,
        check_apertures: bool = True,
        settings: RayFanSettings | None = None,
    ):
        """Create a new Ray Fan analysis.

        See Also
        --------
        RayFanSettings : Settings for the Ray Fan analysis.
        """
        super().__init__(settings or RayFanSettings(), locals())

    def run_analysis(self) -> RayFanResult | None:
        """Run the Ray Fan analysis."""
        self.analysis.field = self.settings.field
        self.analysis.set_surface(self.settings.surface)
        self.analysis.wavelength = self.settings.wavelength
        self.analysis.Settings.PlotScale = self.settings.plot_scale
        self.analysis.Settings.NumberOfRays = self.settings.number_of_rays
        self.analysis.Settings.Tangential = constants.process_constant(
            constants.Analysis.Settings.Fans.TangentialAberrationComponent, self.settings.tangential
        )
        self.analysis.Settings.Sagittal = constants.process_constant(
            constants.Analysis.Settings.Fans.SagittalAberrationComponent, self.settings.sagittal
        )
        self.analysis.Settings.UseDashes = self.settings.use_dashes
        self.analysis.Settings.VignettedPupil = self.settings.vignetted_pupil
        self.analysis.Settings.CheckApertures = self.settings.check_apertures

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results

        return self.get_data_series()

    def get_data_series(self) -> RayFanResult | None:
        """Get the data series from the Ray Fan analysis."""
        ray_fan_description_regex = re.compile(
            rf"(?P<direction>sagittal|tangential) fan, field number (?P<field>\d+) = "
            rf"(?P<coordinate>\d+\{config.DECIMAL_POINT}\d+) \((?P<unit>.+)\)",
            re.IGNORECASE,
        )

        if self.analysis.Results.NumberOfDataSeries <= 0:
            return None

        tangential_fans = []
        sagittal_fans = []

        for i in range(self.analysis.Results.NumberOfDataSeries):
            data_series = self.analysis.Results.GetDataSeries(i)

            match = ray_fan_description_regex.match(data_series.Description)

            if match is None:
                raise ValueError(f"Could not parse description: {data_series.Description}")

            index = pd.Index(data_series.XData.Data, name=data_series.XLabel)
            columns = [atox(label, float) for label in data_series.SeriesLabels]
            data = np.array(data_series.YData.Data)

            fan_data = FanData(
                field_number=int(match.group("field")),
                field_coordinate=UnitField(value=atox(match.group("coordinate"), float), unit=match.group("unit")),
                data=DataFrame(index=index, columns=columns, data=data),
            )

            if match.group("direction").lower() == "tangential":
                tangential_fans.append(fan_data)
            else:
                sagittal_fans.append(fan_data)

        return RayFanResult(tangential=tangential_fans, sagittal=sagittal_fans)
