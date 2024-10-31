import pytest

import zospy.api.constants as constants


class TestProcessConstant:
    def test_process_constant_converts_string_to_constant(self, zos):
        processed_constant = constants.process_constant(constants.Analysis.AnalysisIDM, "DetectorViewer")

        assert processed_constant == constants.Analysis.AnalysisIDM.DetectorViewer

    def test_process_constant_converts_constant_to_constant(self, zos):
        processed_constant = constants.process_constant(
            constants.SystemData.ZemaxApertureType, constants.SystemData.ZemaxApertureType.FloatByStopSize
        )

        assert processed_constant == constants.SystemData.ZemaxApertureType.FloatByStopSize

    @pytest.mark.parametrize("none", [None, "None", "None_"])
    def test_process_constant_converts_none_to_constant(self, none, zos):
        processed_constant = constants.process_constant(constants.Editors.SolveType, none)

        assert processed_constant == constants.Editors.SolveType.None_

    def test_process_constant_incorrect_string_raises_valueerror(self, zos):
        with pytest.raises(ValueError):
            constants.process_constant(constants.ZOSAPI_Mode, "NonExistentMode")

    def test_process_constant_incorrect_constant_raises_valueerror(self, zos):
        with pytest.raises(ValueError):
            constants.process_constant(constants.Common.SettingsDataType, constants.SystemData.FieldColumn.Comment)
