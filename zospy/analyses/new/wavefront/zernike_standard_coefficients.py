from __future__ import annotations

from typing import Annotated, TypedDict

from pydantic import Field

from zospy.analyses.new.base import AnalysisData, AnalysisWrapper
from zospy.analyses.new.decorators import analysis_result, analysis_settings
from zospy.analyses.new.parsers import ZospyTransformer
from zospy.analyses.new.parsers.transformers import SimpleField
from zospy.analyses.new.parsers.types import UnitField
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling


class _ZernikeStandardCoefficient(TypedDict):
    value: float
    formula: str


class ZernikeStandardCoefficientsTransformer(ZospyTransformer):
    def coefficients(self, args):
        return SimpleField("Coefficients", dict(args))

    def zernike_coefficient(self, args):
        index, value, formula = args

        return SimpleField(index, _ZernikeStandardCoefficient(value=value, formula=formula))


@analysis_result
class ZernikeStandardCoefficient:
    value: float
    formula: str


@analysis_result
class IntegrationData:
    rms_to_chief: UnitField = Field(alias="RMS (to chief)")
    rms_to_centroid: UnitField = Field(alias="RMS (to centroid)")
    variance: UnitField = Field(alias="Variance")
    strehl_ratio: float = Field(alias="Strehl Ratio (Est)")


@analysis_result
class ZernikeStandardCoefficientsResult:
    subaperture_decenter_sx: float | None = Field(alias="Subaperture decenter Sx", default=None)
    subaperture_decenter_sy: float | None = Field(alias="Subaperture decenter Sy", default=None)
    subaperture_radius_sr: float | None = Field(alias="Subaperture radius Sr", default=None)
    surface: str | int = Field(alias="Surface")
    field: UnitField = Field(alias="Field")
    wavelength: UnitField = Field(alias="Wavelength")
    peak_to_valley_to_chief: UnitField = Field(alias="Peak to Valley (to chief)")
    peak_to_valley_to_centroid: UnitField = Field(alias="Peak to Valley (to centroid)")

    from_integration_of_the_rays: IntegrationData = Field(alias="From integration of the rays")
    from_integration_of_the_fitted_coefficients: IntegrationData = Field(
        alias="From integration of the fitted coefficients"
    )

    rms_fit_error: UnitField = Field(alias="RMS fit error")
    maximum_fit_error: UnitField = Field(alias="Maximum fit error")

    coefficients: dict[int, ZernikeStandardCoefficient] = Field(alias="Coefficients")


@analysis_settings
class ZernikeStandardCoefficientsSettings:
    sampling: str = Field(default="64x64", description="Sampling grid size")
    maximum_term: int = Field(default=37, ge=0, description="Maximum term")
    wavelength: str | Annotated[int, Field(ge=0)] = Field(default=1, description="Wavelength")
    field: str | Annotated[int, Field(ge=0)] = Field(default=1, description="Field")
    reference_opd_to_vertex: bool = Field(default=False, description="Reference OPD to vertex")
    surface: str | Annotated[int, Field(ge=0)] = Field(default="Image", description="Surface")
    sx: float = Field(default=0.0, description="Sx")
    sy: float = Field(default=0.0, description="Sy")
    sr: float = Field(default=0.0, description="Sr")


class ZernikeStandardCoefficients(
    AnalysisWrapper[ZernikeStandardCoefficientsResult, ZernikeStandardCoefficientsSettings]
):
    TYPE = "ZernikeStandardCoefficients"

    _needs_text_output_file = True

    def __init__(
        self,
        sampling: str = "64x64",
        maximum_term: int = 37,
        wavelength: str | int = 1,
        field: str | int = 1,
        reference_opd_to_vertex: bool = False,
        surface: str | int = "Image",
        sx: float = 0.0,
        sy: float = 0.0,
        sr: float = 0.0,
        settings: ZernikeStandardCoefficientsSettings | None = None,
    ):
        super().__init__(settings or ZernikeStandardCoefficientsSettings(), locals())

    def run_analysis(self, *args, **kwargs) -> AnalysisData:
        self.analysis.Settings.SampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.sampling)
        )
        self.analysis.Settings.MaximumNumberOfTerms = self.settings.maximum_term
        self.analysis.wavelength = self.settings.wavelength
        self.analysis.field = self.settings.field
        self.analysis.Settings.ReferenceOBDToVertex = (
            self.settings.reference_opd_to_vertex
        )  # ToDo: Monitor name with zemax updates
        self.analysis.set_surface(self.settings.surface)
        self.analysis.Settings.Sx = self.settings.sx
        self.analysis.Settings.Sy = self.settings.sy
        self.analysis.Settings.Sr = self.settings.sr

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        result = self.parse_output(
            "zernike_standard_coefficients",
            transformer=ZernikeStandardCoefficientsTransformer,
            result_type=ZernikeStandardCoefficientsResult,
        )

        return result
