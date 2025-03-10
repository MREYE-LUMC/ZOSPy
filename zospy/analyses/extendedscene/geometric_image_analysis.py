"""Geometric Image Analysis."""

from __future__ import annotations

from typing import Annotated, Literal, Union

import pandas as pd
from pandas import DataFrame
from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import WavelengthNumber, ZOSAPIConstant  # noqa: TCH001
from zospy.api import constants

__all__ = ("GeometricImageAnalysis", "GeometricImageAnalysisSettings")

from zospy.utils import zputils


@analysis_settings
class GeometricImageAnalysisSettings:
    """Settings for the Geometric Image Analysis.

    For an in depth explanation of the parameters, see the OpticStudio user manual.

    Attributes
    ----------
    wavelength : str | int
        The wavelength to use in the analysis. Either 'All' or an integer specifying the wavelength number. Defaults to
        'All'.
    field : int
        The field to use in the analysis. Should be an integer specifying the field number. Defaults to 1.
    surface : str | int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    field_size : float
        The width of the image in field coordinates. Defaults to 0.
    image_size : float
        When show_as is set to 'SpotDiagram', this defines the size of the scale bar superimposed on the image. Else, it
         defines the size of the detector used to capture the rays. Defaults to 50.
    file : str
        The image file used for the analysis. Must be an .IMA of .BIM file and reside in the OpticStudio images folder.
        Defaults to 'LETTERF.IMA'.
    rotation : float
        The rotation angle in degrees. Defaults to 0.
    rays_x_1000 : int
        The approximate amount of rays that are traced. See OpticStudio manual for further clarification. Defaults to
        10.
    show_as : str | constants.Analysis.GiaShowAsTypes
        Defines how the result is displayed in OpticStudio. Defaults to 'Surface'. Note that 'SpotDiagram' is not
        implemented.
    source : str | constants.Analysis.Settings.SourceGia
        Specifies how the source is defined. Defaults to 'Uniform'.
    number_of_pixels : int
        The number of pixels across the width of the image. Not used when show_as is set to 'SpotDiagram'. Defaults to
        100.
    row_column_number : int | str
        An integer defining the row or column number used when show_as is either 'CrossX' or 'CrossY'. Also accepts
        'Center'. Defaults to 'Center'.
    na : float
        The numerical aperture cut-off. Ignored if set to 0. Defaults to 0.
    total_watts : float
        The total power in watts. Defaults to 1.
    parity : str | constants.Analysis.Settings.Parity
        Defines how the object would appear in object space. Defaults to 'Even'.
    reference : str | constants.Analysis.Settings.ReferenceGia
        Defines the reference coordinate for the center of the plot. Defaults to 'ChiefRay'.
    use_symbols : bool
        Defines whether the plot uses symbols. Only used when show-as is set to 'SpotDiagram'. Defaults to False.
    use_polarization : bool
        Defines whether polarization is considered. Defaults to False.
    remove_vignetting_factors : bool
        Defines whether vignetting factors are automatically removed. Defaults to True.
    scatter_rays : bool
        Defines whether rays are scattered by surfaces with scattering properties. Defaults to False.
    delete_vignetted : False
        Defines whether rays vignetted by any surface are drawn. Defaults to False.
    use_pixel_interpolation : bool
        Defines whether pixel interpolation is used. This setting has no effect when show-as is set to 'SpotDiagram'.
        Defaults to False.
    save_as_bim_file : str
        Defines the filename used to save the output image as BIM file. This file will be stored in the OpticStudio
        images folder. The filename should include the .BIM extension. If set to '', the image will not be saved. Not
        used when show_as is set to 'SpotDiagram.  Defaults to ''.
    """

    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number or 'All'")
    field: int = Field(default=1, gt=0, description="Field number")
    surface: Literal["Image"] | Annotated[int, Field(gt=0)] = Field(default="Image", description="Surface")
    field_size: float = Field(default=0, description="Field size")
    image_size: float = Field(default=50, description="Field size")
    file: str = Field(default="LETTERF.IMA", description="Image file used for the analysis")
    rotation: float = Field(default=0, description="Rotation angle in degrees")
    rays_x_1000: int = Field(default=10, gt=1, description="Approximate number of traced rays (x 1000)")
    show_as: ZOSAPIConstant("Analysis.GiaShowAsTypes") = Field(default="Surface", description="Show As")
    source: ZOSAPIConstant("Analysis.Settings.SourceGia") = Field(default="Uniform", description="Source")
    number_of_pixels: int = Field(default=100, ge=1, description="Number of pixels")
    row_column_number: Literal["Center"] | Annotated[int, Field(gt=0)] = Field(
        default="Center", description="Row or column number"
    )
    na: float = Field(default=0, description="Numerical aperture cut-off")
    total_watts: float = Field(default=1, gt=0, description="Total watts")
    parity: ZOSAPIConstant("Analysis.Settings.Parity") = Field(default="Even", description="Parity")
    reference: ZOSAPIConstant("Analysis.Settings.ReferenceGia") = Field(default="ChiefRay", description="Chief Ray")
    use_symbols: bool = Field(default=False, description="Use symbols")
    use_polarization: bool = Field(default=False, description="Use polarization")
    remove_vignetting_factors: bool = Field(default=True, description="Remove vignetting factors")
    scatter_rays: bool = Field(default=False, description="Scatter rays")
    delete_vignetted: bool = Field(default=False, description="Delete vignetted")
    use_pixel_interpolation: bool = Field(default=False, description="Use pixel interpolation")
    save_as_bim_file: str = Field(default="", description="Filename used to save output as BIM file")


class GeometricImageAnalysis(
    BaseAnalysisWrapper[Union[DataFrame, None], GeometricImageAnalysisSettings], analysis_type="GeometricImageAnalysis"
):
    """Geometric Image Analysis."""

    def __init__(
        self,
        *,
        wavelength: Literal["All"] | int = "All",
        field: int = 1,
        surface: Literal["Image"] | int = "Image",
        field_size: float = 0,
        image_size: float = 50,
        file: str = "LETTERF.IMA",
        rotation: float = 0,
        rays_x_1000: int = 10,
        show_as: constants.Analysis.GiaShowAsTypes | str = "Surface",
        source: constants.Analysis.Settings.SourceGia | str = "Uniform",
        number_of_pixels: int = 100,
        row_column_number: Literal["Center"] | int = "Center",
        na: float = 0,
        total_watts: float = 1,
        parity: constants.Analysis.Settings.Parity | str = "Even",
        reference: constants.Analysis.Settings.ReferenceGia | str = "ChiefRay",
        use_symbols: bool = False,
        use_polarization: bool = False,
        remove_vignetting_factors: bool = True,
        scatter_rays: bool = False,
        delete_vignetted: bool = False,
        use_pixel_interpolation: bool = False,
        save_as_bim_file: str = "",
        settings: GeometricImageAnalysisSettings | None = None,
    ):
        """Create a new Geometric Image Analysis.

        See Also
        --------
        GeometricImageAnalysisSettings : Settings for the Geometric Image Analysis analysis.
        """
        super().__init__(settings_kws=locals())

    def get_data_grid(self, minx=None, miny=None) -> pd.DataFrame | None:
        """Get the data grids from the analysis result.

        Returns
        -------
        pd.DataFrame | None
            The data grids from the analysis result, or None if there are no data grids.
        """
        # Obtain correct origin for datagrid as there is a bug in the API
        # See also https://community.zemax.com/zos-api-12/incorrect-datagrid-miny-for-geometric-image-analysis-5426
        minx = -self.analysis.Settings.ImageSize / 2
        miny = -self.analysis.Settings.ImageSize / 2

        # Get data
        data = [
            zputils.unpack_datagrid(self.analysis.Results.DataGrids[i], minx=minx, miny=miny, cell_origin="bottom_left")
            for i in range(self.analysis.Results.NumberOfDataGrids)
        ]

        return self._process_data_series_or_grid(data)

    def run_analysis(self) -> DataFrame | None:
        """Run the FFT Through Focus MTF analysis."""
        self.analysis.set_wavelength(
            0 if self.settings.wavelength == "All" else self.settings.wavelength
        )  # TODO track with future releases
        self.analysis.set_field(self.settings.field)
        self.analysis.set_surface(self.settings.surface)
        self.analysis.Settings.FieldSize = self.settings.field_size
        self.analysis.Settings.ImageSize = self.settings.image_size
        self.analysis.Settings.File = self.settings.file
        self.analysis.Settings.Rotation = self.settings.rotation
        self.analysis.Settings.RaysX1000 = self.settings.rays_x_1000
        self.analysis.Settings.ShowAs = constants.process_constant(
            constants.Analysis.GiaShowAsTypes, self.settings.show_as
        )
        self.analysis.Settings.Source = constants.process_constant(
            constants.Analysis.Settings.SourceGia, self.settings.source
        )

        if str(self.analysis.Settings.ShowAs) in ("CrossX", "CrossY"):
            if self.settings.row_column_number == "Center":
                self.analysis.Settings.UseColumnRowCenter()
            else:
                self.analysis.Settings.RowColumnNumber = self.settings.row_column_number
        if str(self.analysis.Settings.ShowAs) != "SpotDiagram":
            self.analysis.Settings.NumberOfPixels = self.settings.number_of_pixels
        if str(self.analysis.Settings.ShowAs) == "SpotDiagram":
            self.analysis.Settings.UseSymbols = self.settings.use_symbols

        self.analysis.Settings.NA = self.settings.na
        self.analysis.Settings.TotalWatts = self.settings.total_watts
        self.analysis.Settings.Parity = constants.process_constant(
            constants.Analysis.Settings.Parity, self.settings.parity
        )
        self.analysis.Settings.Reference = constants.process_constant(
            constants.Analysis.Settings.ReferenceGia, self.settings.reference
        )

        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.RemoveVignettingFactors = self.settings.remove_vignetting_factors
        self.analysis.Settings.ScatterRays = self.settings.scatter_rays
        self.analysis.Settings.DeleteVignetted = self.settings.delete_vignetted
        self.analysis.Settings.UsePixelInterpolation = self.settings.use_pixel_interpolation
        self.analysis.Settings.SaveAsBIMFile = self.settings.save_as_bim_file

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        return self.get_data_grid()
