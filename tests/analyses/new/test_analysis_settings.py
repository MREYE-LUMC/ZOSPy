import re
from inspect import getsource, getsourcelines

import pytest
from zospy.analyses.new.base import BaseAnalysisWrapper, new_analysis
from zospy.analyses.new.systemviewers.base import SystemViewerWrapper
from zospy.api import constants
from zospy.api.constants import process_constant

analysis_wrapper_classes = BaseAnalysisWrapper.__subclasses__()
analysis_wrapper_classes.remove(SystemViewerWrapper)

REGEX_SETTING = re.compile(r"\s*self\.analysis\.Settings\.(?P<setting>\w+)")


@pytest.mark.parametrize("analysis_wrapper", analysis_wrapper_classes)
def test_settings_exist(empty_system, analysis_wrapper):
    if analysis_wrapper.MODE == "Nonsequential":
        empty_system.make_nonsequential()

    analysis = new_analysis(empty_system, process_constant(constants.Analysis.AnalysisIDM, analysis_wrapper.TYPE))
    source = getsource(analysis_wrapper.run_analysis)

    settings = REGEX_SETTING.findall(source)

    for setting in settings:
        assert hasattr(analysis.Settings, setting)
