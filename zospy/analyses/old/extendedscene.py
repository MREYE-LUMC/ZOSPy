"""Zemax OpticStudio analyses from the Extended Scene Analysis category."""

from __future__ import annotations

from typing import Literal

import pandas as pd

from zospy import utils
from zospy.analyses.old.base import AnalysisResult, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def geometric_image_analysis(
    oss: OpticStudioSystem,
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
    oncomplete: OnComplete | str = OnComplete.Close,
) -> AnalysisResult:
    """Geometric image analysis.

    See the OpticStudio documentation for a more in depth description of most parameters.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
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
    show_as : constants.Analysis.GiaShowAsTypes | str
        Defines how the result is displayed in OpticStudio. Defaults to 'Surface'. Note that 'SpotDiagram' is not
        implmented.
    source : constants.Analysis.Settings.SourceGia | str
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
    parity : constants.Analysis.Settings.Parity | str
        Defines how the object would appear in object space. Defaults to 'Even'.
    reference : constants.Analysis.Settings.ReferenceGia | str
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
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        A Geometric Image Analysis result.

    Raises
    ------
    NotImplementedError
        When show_as is set to SpotDiagram.
    """
    if str(show_as) == "SpotDiagram":
        raise NotImplementedError("Geometric Image Analysis with show_as set to SpotDiagram is not implemented.")

    analysis_type = constants.Analysis.AnalysisIDM.GeometricImageAnalysis

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    # Adjust settings
    analysis.set_wavelength(wavelength)
    analysis.set_field(field)
    analysis.set_surface(surface)
    analysis.Settings.FieldSize = field_size
    analysis.Settings.ImageSize = image_size
    analysis.Settings.File = file
    analysis.Settings.Rotation = rotation
    analysis.Settings.RaysX1000 = rays_x_1000
    analysis.Settings.ShowAs = constants.process_constant(constants.Analysis.GiaShowAsTypes, show_as)
    analysis.Settings.Source = constants.process_constant(constants.Analysis.Settings.SourceGia, source)

    if str(show_as) in ("CrossX", "CrossY"):
        if row_column_number == "Center":
            analysis.Settings.UseColumnRowCenter()
        else:
            analysis.Settings.RowColumnNumber = row_column_number
    if str(show_as) != "SpotDiagram":
        analysis.Settings.NumberOfPixels = number_of_pixels
    if str(show_as) == "SpotDiagram":
        analysis.Settings.UseSymbols = use_symbols

    analysis.Settings.NA = na
    analysis.Settings.TotalWatts = total_watts
    analysis.Settings.Parity = constants.process_constant(constants.Analysis.Settings.Parity, parity)
    analysis.Settings.Reference = constants.process_constant(constants.Analysis.Settings.ReferenceGia, reference)

    analysis.Settings.UsePolarization = use_polarization
    analysis.Settings.RemoveVignettingFactors = remove_vignetting_factors
    analysis.Settings.ScatterRays = scatter_rays
    analysis.Settings.DeleteVignetted = delete_vignetted
    analysis.Settings.UsePixelInterpolation = use_pixel_interpolation
    analysis.Settings.SaveAsBIMFile = save_as_bim_file

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)
    settings.loc["Field"] = analysis.get_field()
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["Surface"] = analysis.Settings.Surface.GetSurfaceNumber()
    settings.loc["FieldSize"] = analysis.Settings.FieldSize
    settings.loc["ImageSize"] = analysis.Settings.ImageSize
    settings.loc["File"] = analysis.Settings.File
    settings.loc["Rotation"] = analysis.Settings.Rotation
    settings.loc["RaysX1000"] = analysis.Settings.RaysX1000
    settings.loc["ShowAs"] = str(analysis.Settings.ShowAs)
    settings.loc["Source"] = str(analysis.Settings.Source)
    if str(analysis.Settings.ShowAs) != "SpotDiagram":
        settings.loc["NumberOfPixels"] = analysis.Settings.NumberOfPixels
    if str(analysis.Settings.ShowAs) in ("CrossX", "CrossY"):
        if analysis.Settings.RowColumnNumber == 0:
            settings.loc["Row"] = "Center"
        else:
            settings.loc["Row"] = analysis.Settings.RowColumnNumber
    settings.loc["NA"] = analysis.Settings.NA
    settings.loc["TotalWatts"] = analysis.Settings.TotalWatts
    settings.loc["Parity"] = str(analysis.Settings.Parity)
    settings.loc["Reference"] = str(analysis.Settings.Reference)
    if str(analysis.Settings.ShowAs) == "SpotDiagram":
        settings.loc["UseSymbols"] = analysis.Settings.UseSymbols
    settings.loc["UsePolarization"] = analysis.Settings.UsePolarization
    settings.loc["RemoveVignettingFactors"] = analysis.Settings.RemoveVignettingFactors
    settings.loc["ScatterRays"] = analysis.Settings.ScatterRays
    settings.loc["DeleteVignetted"] = analysis.Settings.DeleteVignetted
    settings.loc["UsePixelInterpolation"] = analysis.Settings.UsePixelInterpolation
    settings.loc["SaveAsBIMFile"] = analysis.Settings.SaveAsBIMFile

    # Get data and unpack
    data = []
    for ii in range(analysis.Results.NumberOfDataGrids):
        data.append(utils.zputils.unpack_datagrid(analysis.Results.DataGrids[ii],
                                                  # pass "center" and None for consistency with older ZOSPy versions
                                                  cell_origin="center", label_rounding=None))

    if len(data) == 0:
        data = pd.DataFrame()
    elif len(data) == 1:
        data = data[0]
    else:
        data = pd.concat(data, axis=1)

    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)
