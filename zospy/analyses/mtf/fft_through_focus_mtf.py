"""FFT Through Focus MTF analysis."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Annotated, Literal, Union

import numpy as np
import pandas as pd
from pydantic import Field, RootModel

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result, analysis_settings
from zospy.analyses.parsers.types import UnitField, ValidatedDataFrame, ZOSAPIConstant
from zospy.api import config, constants
from zospy.utils.pyutils import atox
from zospy.utils.zputils import standardize_sampling

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = ("FFTThroughFocusMTF", "FFTThroughFocusMTFSettings")


@analysis_settings
class FFTThroughFocusMTFSettings:
    """Settings for the FFT Through Focus MTF analysis.

    For an in depth explanation of the parameters, see the OpticStudio user manual.

    Attributes
    ----------
    sampling : str | int
        The pupil sampling, either string (e.g. "64x64") or int. Integers will be treated as a ZOSAPI Constants
        integer and must be greater than or equal to 0. Defaults to "64x64".
    delta_focus : float
        The Z-axis range or optical power range, depending on the optical system. Defaults to 0.1.
    frequency : float
        The spatial frequency for which the MTF is calculated. Defaults to 0.
    number_of_steps : int
        The number of steps in the focus range. Defaults to 5.
    wavelength : int | str
        The wavelength to use in the MTF. Either 'All' or an integer specifying the wavelength number.
    field : str | int
        The field to use in the MTF. Either 'All' or an integer specifying the field number.
    mtf_type : zospy.constants.Analysis.Settings.Mtf.MtfTypes.Modulation
        The MTF type (e.g. `Modulation`) that is calculated.
    use_polarization : bool
        Use polarization. Defaults to False.
    use_dashes : bool
        Use dashes. Defaults to False.
    """

    sampling: str | Annotated[int, Field(ge=0)] = Field(default="64x64", description="Sampling grid size")
    delta_focus: float = Field(default=0.1, description="Focus step size")
    frequency: float = Field(default=0, description="Frequency")
    number_of_steps: int = Field(default=5, ge=0, description="Number of steps")
    wavelength: Literal["All"] | Annotated[int, Field(gt=0)] = Field(
        default="All", description="Wavelength number or 'All'"
    )
    field: Literal["All"] | Annotated[int, Field(gt=0)] = Field(default="All", description="Field number or 'All'")
    mtf_type: ZOSAPIConstant("Analysis.Settings.Mtf.MtfTypes") = Field(default="Modulation", description="MTF type")
    use_polarization: bool = Field(default=False, description="Use polarization")
    use_dashes: bool = Field(default=False, description="Use dashes")


@analysis_result
class FFTThroughFocusMTFData:
    field_coordinate: UnitField[tuple[float, float]]
    data: ValidatedDataFrame

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the data to a Pandas DataFrame.

        In addition to the columns from FFTThroughFocusMTFData.data, the returned DataFrame has the following columns:

        - FieldX: The field x coordinate
        - FieldY: The field y coordinate

        Returns
        -------
        DataFrame
            The data in long format.
        """
        df: pd.DataFrame = self.data.copy().reset_index()

        df.insert(0, "FieldX", self.field_coordinate.value[0])
        df.insert(1, "FieldY", self.field_coordinate.value[1])

        return df


class FFTThroughFocusMTFResult(RootModel[list[FFTThroughFocusMTFData]]):
    def __iter__(self) -> Iterator[FFTThroughFocusMTFData]:
        return iter(self.root)

    def __getitem__(self, item) -> FFTThroughFocusMTFData:
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the data to a Pandas DataFrame.

        The separate dataframes for each field are combined in a DataFrame in long format.
        In addition to the columns for each wavelength, the returned DataFrame has the following columns:

        - Direction: The direction of the fan, either 'Tangential' or 'Sagittal'.
        - Field Number: The field number.
        - Field: The field coordinate.

        Returns
        -------
        DataFrame
            The data in long format.
        """
        return pd.concat([fft.to_dataframe() for fft in self], ignore_index=True).reset_index(drop=True)


class FFTThroughFocusMTF(
    BaseAnalysisWrapper[Union[FFTThroughFocusMTFResult, None], FFTThroughFocusMTFSettings],
    analysis_type="FftThroughFocusMtf",
    needs_config_file=True,
):
    """FFT Through Focus MTF analysis."""

    def __init__(
        self,
        *,
        sampling: str | int = "64x64",
        delta_focus: float = 0.1,
        frequency: float = 0,
        number_of_steps: int = 5,
        wavelength: int | Literal["All"] = "All",
        field: int | Literal["All"] = "All",
        mtf_type: constants.Analysis.Settings.Mtf.MtfTypes | str = "Modulation",
        use_polarization: bool = False,
        use_dashes: bool = False,
    ):
        """Create a new FFT Through Focus MTF analysis.

        See Also
        --------
        FFTThroughFocusMTFSettings : Settings for the FFT Through Focus MTF analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> FFTThroughFocusMTFResult | None:
        """Run the FFT Through Focus MTF analysis."""
        self.analysis.Settings.SampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.sampling)
        )
        self.analysis.Settings.DeltaFocus = self.settings.delta_focus
        self.analysis.Settings.Frequency = self.settings.frequency
        self.analysis.Settings.NumberOfSteps = self.settings.number_of_steps
        self.analysis.set_wavelength(self.settings.wavelength)
        self.analysis.set_field(self.settings.field)
        self.analysis.Settings.Type = constants.process_constant(
            constants.Analysis.Settings.Mtf.MtfTypes, self.settings.mtf_type
        )
        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.UseDashes = self.settings.use_dashes

        self._correct_mtf_type_api_bug()

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        return self.get_data_series()

    def get_data_series(self) -> FFTThroughFocusMTFResult | None:
        """Get the data series from the FFT Through Focus MTF analysis."""
        re_float = rf"-?\d+\{config.DECIMAL_POINT}\d+"
        fft_through_focus_mtf_description_regex = re.compile(
            rf"Field: "
            rf"(?P<field_1>{re_float})(?:, (?P<field_2>{re_float}))? "
            r"(?P<unit>\(.+?\)|\S.*)?",  # unit can, but might not have parentheses
            re.IGNORECASE,
        )

        if self.analysis.Results.NumberOfDataSeries <= 0:
            return None

        fft_results = []
        for i in range(self.analysis.Results.NumberOfDataSeries):
            data_series = self.analysis.Results.GetDataSeries(i)

            match = fft_through_focus_mtf_description_regex.match(data_series.Description)

            if match is None:
                raise ValueError(f"Could not parse description: {data_series.Description}")

            index = pd.Index(data_series.XData.Data, name=data_series.XLabel)
            columns = data_series.SeriesLabels
            data = np.array(data_series.YData.Data)

            if match.group("field_2"):
                field_x = atox(match.group("field_1"), float)
                field_y = atox(match.group("field_2"), float)
            else:  # field 1 corresponds to y
                field_x = 0.0
                field_y = atox(match.group("field_1"), float)

            coordinate = (field_x, field_y)

            fft_data = FFTThroughFocusMTFData(
                field_coordinate=UnitField(value=coordinate, unit=match.group("unit")),
                data=pd.DataFrame(index=index, columns=columns, data=data),
            )

            fft_results.append(fft_data)

        return FFTThroughFocusMTFResult.model_validate(fft_results)

    def _correct_mtf_type_api_bug(self) -> None:
        """Correction for an API bug in OpticStudio versions < 21.2.

        In these versions, the MTF Type cannot be set through the ZOS-API for the FFT Through Focus MTF
        See also: https://community.zemax.com/zos-api-12/zos-api-setting-mtf-property-type-not-working-730

        Returns
        -------
        None
        """
        if self.oss.ZOS.version < "21.2.0":
            config_file = str(self.config_file)

            self.analysis.Settings.SaveTo(config_file)

            self.analysis.Settings.ModifySettings(
                config_file,
                "TFM_TYPE",
                str(int(constants.process_constant(constants.Analysis.Settings.Mtf.MtfTypes, self.settings.mtf_type))),
            )
            self.analysis.Settings.LoadFrom(config_file)
