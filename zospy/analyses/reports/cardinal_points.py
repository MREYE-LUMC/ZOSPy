"""Cardinal points analysis."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, model_validator
from pydantic_core._pydantic_core import PydanticCustomError

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result, analysis_settings
from zospy.analyses.parsers import ZospyTransformer
from zospy.analyses.parsers.transformers import SimpleField

__all__ = ("CardinalPoints", "CardinalPointsSettings")


class CardinalPointsTransformer(ZospyTransformer):
    def cardinal_points(self, args):
        header, *values = args

        updated_values = [SimpleField(v.name, dict(zip(header, v.value))) for v in values]

        return SimpleField("Cardinal Points", self.dict(updated_values))

    def cardinal_point(self, args):
        name, *values = args

        return SimpleField(str(name), values)


@analysis_result
class CardinalPoint:
    object: float = Field(alias="Object Space")
    image: float = Field(alias="Image Space")


@analysis_result
class CardinalPointSpecification:
    focal_length: CardinalPoint = Field(alias="Focal Length")
    focal_planes: CardinalPoint = Field(alias="Focal Planes")
    principal_planes: CardinalPoint = Field(alias="Principal Planes")
    anti_principal_planes: CardinalPoint = Field(alias="Anti-Principal Planes")
    nodal_planes: CardinalPoint = Field(alias="Nodal Planes")
    anti_nodal_planes: CardinalPoint = Field(alias="Anti-Nodal Planes")


@analysis_result
class CardinalPointsResult:
    starting_surface: int = Field(alias="Starting surface")
    ending_surface: int = Field(alias="Ending surface")
    wavelength: float = Field(alias="Wavelength")
    orientation: str = Field(alias="Orientation")
    lens_units: str = Field(alias="Lens units")
    cardinal_points: CardinalPointSpecification = Field(alias="Cardinal Points")


@analysis_settings
class CardinalPointsSettings:
    """Settings for the Cardinal Points analysis.

    Attributes
    ----------
    surface_1 : int
        The surface number corresponding to the first surface of the analyzed system. Defaults to 1.
    surface_2 : int
        The surface number corresponding to the last surface of the analyzed system, or "Image". Defaults to "Image".
    wavelength : int
        The wavelength number. Defaults to 1.
    orientation : Literal["Y-Z", "X-Z"]
        The orientation along which the cardinal points are calculated. Must be one of "X-Z", "Y-Z". Defaults to "Y-Z".
    """

    surface_1: Annotated[int, Field(ge=1)] = Field(default=1, description="First surface of the analyzed system")
    surface_2: Annotated[int, Field(ge=2)] | Literal["Image"] = Field(
        default="Image", description="Last surface of the analyzed system"
    )
    wavelength: int = Field(default=1, ge=1, description="Wavelength number")
    orientation: Literal["Y-Z", "X-Z"] = Field(
        default="Y-Z", description="Orientation along which the cardinal points are calculated"
    )

    @model_validator(mode="after")
    def validate_surfaces(self):
        """Validate that surface_1 is less than surface_2."""
        if isinstance(self.surface_1, int) and isinstance(self.surface_2, int) and self.surface_1 >= self.surface_2:
            raise PydanticCustomError(
                "invalid_surface_number",
                "surface_1 must be less than surface_2, but got {surface_1} >= {surface_2}",
                {"surface_1": self.surface_1, "surface_2": self.surface_2},
            )

        return self


class CardinalPoints(
    BaseAnalysisWrapper[CardinalPointsResult, CardinalPointsSettings],
    analysis_type="CardinalPoints",
    needs_text_output_file=True,
    needs_config_file=True,
):
    """Cardinal points analysis."""

    def __init__(
        self,
        *,
        surface_1: int = 1,
        surface_2: int | Literal["Image"] = "Image",
        wavelength: int = 1,
        orientation: Literal["Y-Z", "X-Z"] = "Y-Z",
    ):
        """Create a new Cardinal Points analysis.

        See Also
        --------
        CardinalPointsSettings : Settings for the Cardinal Points analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> CardinalPointsResult:
        """Run the Cardinal Points analysis."""
        if self.settings.surface_2 == "Image":
            self.settings.surface_2 = self.oss.LDE.NumberOfSurfaces - 1

        settings = self.analysis.GetSettings()
        settings.SaveTo(str(self.config_file))

        settings_bytestring = self.config_file.read_bytes()
        settings_bytearray = bytearray(settings_bytestring)
        settings_bytearray[20] = self.settings.surface_1  # byte 20 maps to the first surface
        settings_bytearray[24] = self.settings.surface_2  # byte 24 maps to the last surface
        settings_bytearray[28] = self.settings.wavelength  # byte 28 maps to the wavelength
        settings_bytearray[32] = 0 if self.settings.orientation == "Y-Z" else 1  # byte 32 maps to the orientation

        self.config_file.write_bytes(settings_bytearray)
        settings.LoadFrom(str(self.config_file))

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Read text file and parse to object
        return self.parse_output(
            "cardinal_points", transformer=CardinalPointsTransformer, result_type=CardinalPointsResult
        )
