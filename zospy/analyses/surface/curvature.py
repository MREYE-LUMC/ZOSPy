"""Surface Curvature analysis."""

from __future__ import annotations

import logging
import re
from typing import Annotated

from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result, analysis_settings
from zospy.analyses.parsers.types import ValidatedDataFrame, ZOSAPIConstant  # noqa: TCH001
from zospy.api import config, constants
from zospy.utils.pyutils import atox
from zospy.utils.zputils import standardize_sampling, unpack_datagrid

__all__ = ("Curvature", "CurvatureSettings")


@analysis_result
class CurvatureResult:
    width: float
    decenter_x: float
    decenter_y: float
    decenter_unit: str
    data: ValidatedDataFrame


@analysis_settings
class CurvatureSettings:
    """Settings for the Curvature analysis.

    Attributes
    ----------
    sampling : str | int
        The size of the used grid, either string (e.g. '65x65') or int. The integer will be treated as if obtained from
        zospy.constants.Analysis.SampleSizes_Pow2Plus1_X. Defaults to '65x65'.
    data : str
        The used data type. Should be one of ['TangentialCurvature', 'SagittalCurvature', 'X_Curvature', 'Y_Curvature']
        or int. The integer will be treated as if obtained from zospy.constants.Analysis.SurfaceCurvatureData. Defaults
        to 'TangentialCurvature'.
    remove : str
        Defines whether a reference volume is removed or not. Should be one of ['None', 'BaseROC', 'BestFitSphere'] or
        int. The integer will be treated as if obtained from zospy.constants.Analysis.RemoveOptions. Defaults
        to 'None'.
    surface : int
        The surface that is te be analyzed. defaults to 1.
    show_as : str
        Defines how the data is displayed in OpticStudio. Should be one of ['Surface', 'Contour', 'GreyScale',
        'InverseGreyScale', 'FalseColor', 'InverseFalseColor'] or int. The integer will be treated as if obtained from
        `zospy.constants.Analysis.ShowAs`. Defaults to 'Contour'.
    off_axis_coordinates : bool
        Defines whether apertures defined in the Surface Properties of the surface are considered or not. Defaults to
        `False`.
    contour_format : str
        The contour format. Only usable when showas == 'Contour'. Defaults to ''.
    bfs_criterion : str | int
        The criterion for BFS removal. Only usable when remove == 'BestFitSphere'. Should be one of ['MinimumVolume',
        'MinimumRMS', 'MinimumRMSWithOffset'] or int. The integer will be treated as if obtained from
        constants.Analysis.BestFitSphereOptions. Defaults to 'MinimumVolume'.
    bfs_reverse_direction : bool
        Defines if the sign of the BFS radius should be reversed or not. Only usable when remove == 'BestFitSphere'
        and bfs_criterion == 'MinimumVolume'. Defaults to `False`.
    """

    sampling: str | Annotated[int, Field(ge=0)] = Field(default="65x65", description="Sampling grid size")
    data: ZOSAPIConstant("Analysis.SurfaceCurvatureData") = Field(
        default="TangentialCurvature", description="Data type"
    )
    remove: ZOSAPIConstant("Analysis.RemoveOptions") = Field(default="None_", description="Reference volume removal")
    surface: int = Field(default=1, description="Surface number")
    show_as: ZOSAPIConstant("Analysis.ShowAs") = Field(default="Contour", description="Data display in OpticStudio")
    off_axis_coordinates: bool = Field(default=False, description="Consider apertures defined in surface properties")
    contour_format: str = Field(default="", description="Contour format")
    bfs_criterion: ZOSAPIConstant("Analysis.BestFitSphereOptions") = Field(
        default="MinimumVolume", description="BFS removal criterion"
    )
    bfs_reverse_direction: bool = Field(default=False, description="Reverse BFS radius sign")


class Curvature(BaseAnalysisWrapper[CurvatureResult, CurvatureSettings], analysis_type="SurfaceCurvature"):
    """Surface Curvature analysis."""

    def __init__(
        self,
        *,
        sampling: str | int = "65x65",
        data: str | constants.Analysis.SurfaceCurvatureData = "TangentialCurvature",
        remove: str | constants.Analysis.RemoveOptions = "None_",
        surface: int = 1,
        show_as: str | constants.Analysis.ShowAs = "Contour",
        off_axis_coordinates: bool = False,
        contour_format: str = "",
        bfs_criterion: str | constants.Analysis.BestFitSphereOptions = "MinimumVolume",
        bfs_reverse_direction: bool = False,
    ):
        """Create a new Curvature analysis.

        See Also
        --------
        CurvatureSettings : Settings for the Curvature analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> list[CurvatureResult] | None:
        """Run the Curvature analysis."""
        self.analysis.Settings.Sampling = getattr(
            constants.Analysis.SampleSizes_Pow2Plus1_X, standardize_sampling(self.settings.sampling)
        )
        self.analysis.Settings.Data = constants.process_constant(
            constants.Analysis.SurfaceCurvatureData, self.settings.data
        )
        self.analysis.Settings.RemoveOption = constants.process_constant(
            constants.Analysis.RemoveOptions, self.settings.remove
        )
        self.analysis.set_surface(self.settings.surface)
        self.analysis.Settings.ShowAs = constants.process_constant(constants.Analysis.ShowAs, self.settings.show_as)
        self.analysis.Settings.ConsiderOffAxisAperture = self.settings.off_axis_coordinates

        if self.analysis.Settings.ShowAs == constants.Analysis.ShowAs.Contour:
            self.analysis.Settings.ContourFormat = self.settings.contour_format

        if self.analysis.Settings.RemoveOption == constants.Analysis.RemoveOptions.BestFitSphere:
            self.analysis.Settings.BestFitSphereOption = constants.process_constant(
                constants.Analysis.BestFitSphereOptions, self.settings.bfs_criterion
            )
            if self.analysis.Settings.BestFitSphereOption == constants.Analysis.BestFitSphereOptions.MinimumVolume:
                self.analysis.Settings.ReverseDirection = self.settings.bfs_reverse_direction

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        return self.get_data_grid()

    def get_data_grid(self) -> CurvatureResult | None:
        """Get the data grids from the Curvature analysis."""
        curvature_description_regex = re.compile(
            rf"Width = (?P<width>\d+(\{config.DECIMAL_POINT}\d+)?), "
            rf"Decenter x = (?P<decenter_x>\d+(\{config.DECIMAL_POINT}\d+)?), "
            rf"y = (?P<decenter_y>\d+(\{config.DECIMAL_POINT}\d+)?) (?P<decenter_unit>\w+)\.",
            re.IGNORECASE,
        )

        if self.analysis.Results.NumberOfDataGrids == 0:
            return None

        if self.analysis.Results.NumberOfDataGrids > 1:
            raise NotImplementedError("Curvature results with multiple data grids are not supported.")

        datagrid = self.analysis.Results.GetDataGrid(0)
        match = curvature_description_regex.match(datagrid.Description)

        if match is None:  # fall back to using exported text files
            logging.warning(
                "Could not obtain description parameters from datagrid.Description, trying to use exported text file"
            )

            self._needs_text_output_file = True
            self._text_output_file, self._remove_text_output_file = self._create_tempfile(None, ".txt")
            match = curvature_description_regex.search(self.get_text_output())

        if match is None:
            raise ValueError(f"Could not parse description: {datagrid.Description}")

        return CurvatureResult(
            width=atox(match.group("width"), float),
            decenter_x=atox(match.group("decenter_x"), float),
            decenter_y=atox(match.group("decenter_y"), float),
            decenter_unit=match.group("decenter_unit"),
            data=unpack_datagrid(datagrid, cell_origin="center"),
        )
