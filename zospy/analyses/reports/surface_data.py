"""Surface Data analysis."""

from __future__ import annotations

from pathlib import Path  # noqa: TCH003
from typing import Annotated, Any

from pydantic import AliasChoices, BeforeValidator, Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result, analysis_settings
from zospy.analyses.parsers.transformers import SimpleField, ZospyTransformer

__all__ = ("SurfaceData", "SurfaceDataSettings")


class SurfaceDataTransformer(ZospyTransformer):
    """Transformer for the output of the Surface Data analysis."""

    def refractive_index_table(self, args):
        """Convert the refractive index table to a list of dictionaries."""
        header, rows = args[0]
        table_records = [dict(zip(header, row)) for row in rows]

        return SimpleField("Refractive Indices", table_records)

    def surface_number(self, n):
        """Extract the surface number from the header."""
        return SimpleField("Surface Number", n)

    def surface_powers(self, args):
        """Convert the surface powers to a dictionary."""
        return SimpleField("Surface Powers", dict(args))


@analysis_result
class EdgeThickness:
    y: float = Field(alias="Y Edge Thick")
    x: float = Field(alias="X Edge Thick")


@analysis_result
class ModelGlass:
    nd: float = Field(alias="nd")
    abbe: float = Field(alias="Abbe")
    dpgf: float = Field(alias="dPgF")


@analysis_result
class RefractiveIndex:
    number: int = Field(alias="#")
    wavelength: float = Field(alias="Wavelength")
    index: float = Field(alias="Index")


@analysis_result
class MaterialData:
    indices: list[RefractiveIndex] = Field(alias="Refractive Indices")
    best_fit_glass: str | None = Field(alias="Best Fit Glass", default=None)
    glass: str | ModelGlass | None = Field(alias=AliasChoices("Model glass", "Glass"), default=None)


def _deserialize_tuple(value: Any) -> tuple[float, ...] | Any:
    """Deserialize a tuple from a string.

    Used for deserialization of JSON-serialized analysis results.
    """
    if isinstance(value, str):
        return tuple(map(float, value.split(",")))

    return value


TupleKey = Annotated[tuple[float, float], BeforeValidator(_deserialize_tuple)]


@analysis_result
class SurfacePower:
    surf: dict[int, float] = Field(alias="Surf")
    power: dict[TupleKey, float] | None = Field(alias="Power", default=None)
    efl: dict[TupleKey, float] | None = Field(alias="EFL", default=None)
    f_number: dict[TupleKey, float] | None = Field(alias="F/#", default=None)


@analysis_result
class SurfacePowers:
    as_situated: SurfacePower = Field(alias="as situated")
    in_air: SurfacePower = Field(alias="in air")


@analysis_result
class SurfaceDataResult:
    """Data for the Surface Data analysis."""

    comment: str | None = Field(alias="Comment", default=None)
    date: str = Field(alias="Date")
    file: Path = Field(alias="File")
    diameter: float = Field(alias="Diameter")
    edge_thickness: EdgeThickness = Field(alias="Edge Thickness")
    material: MaterialData = Field(alias="Index of Refraction")
    lens_units: str = Field(alias="Lens units")
    surface_powers: SurfacePowers = Field(alias="Surface Powers")
    thickness: float = Field(alias="Thickness")
    shape_factor: float | None = Field(alias="Shape Factor", default=None)


@analysis_settings
class SurfaceDataSettings:
    """Settings for the Surface Data analysis.

    Attributes
    ----------
    surface : int
        The surface number that is to be analyzed
    """

    surface: int = Field(default=1, ge=0, description="Surface number to analyze.")


class SurfaceData(
    BaseAnalysisWrapper[SurfaceDataResult, SurfaceDataSettings],
    analysis_type="SurfaceDataSettings",
    needs_text_output_file=True,
    needs_config_file=True,
):
    """Surface Data analysis."""

    def __init__(self, *, surface: int = 1):
        """Create a new Surface Data analysis.

        See Also
        --------
        SurfaceDataSettings : Settings for the Surface Data analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> SurfaceDataResult:
        """Run the Surface Data analysis."""
        settings = self.analysis.GetSettings()
        settings.SaveTo(str(self.config_file))

        settings_bytestring = self.config_file.read_bytes()
        settings_bytearray = bytearray(settings_bytestring)
        settings_bytearray[20] = self.settings.surface  # 20 maps to the selected surface

        self.config_file.write_bytes(settings_bytearray)

        settings.LoadFrom(str(self.config_file))

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Read text file and parse to object
        return self.parse_output(
            "surface_data",
            transformer=SurfaceDataTransformer,
            result_type=SurfaceDataResult,
        )
