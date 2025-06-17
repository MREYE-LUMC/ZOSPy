import re
from inspect import getsource

from zospy.analyses.base import new_analysis
from zospy.api import constants
from zospy.api.constants import process_constant

REGEX_SETTING = re.compile(r"\s*self\.analysis\.Settings\.(?P<setting>\w+)")


def test_settings_exist(empty_system, analysis_wrapper_class):
    if analysis_wrapper_class.MODE == "Nonsequential":
        empty_system.make_nonsequential()

    analysis = new_analysis(
        empty_system,
        process_constant(constants.Analysis.AnalysisIDM, analysis_wrapper_class.TYPE),
    )
    source = getsource(analysis_wrapper_class.run_analysis)

    settings = REGEX_SETTING.findall(source)

    nonexistent_settings = [setting for setting in settings if not hasattr(analysis.Settings, setting)]

    assert not nonexistent_settings, f"Nonexistent settings: {nonexistent_settings}"
