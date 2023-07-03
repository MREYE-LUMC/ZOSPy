import locale
import os
from tempfile import mkstemp

import pytest

import zospy.api.config as _config
from zospy import constants
from zospy.analyses.base import new_analysis
from zospy.analyses.polarization import _get_number_field
from zospy.utils.pyutils import atox, xtoa


class TestNumberToStringConversion:
    @pytest.mark.parametrize(
        "number,expected_output,decimal_point,thousands_separator",
        [
            (1.5, "1.5", ".", ""),
            (1.5, "1,5", ",", ""),
            (1.5, "1.5", ".", ","),
            (1.5, "1,5", ",", "."),
            (1.5, "1.5", ".", None),
            (1.5, "1,5", ",", None),
            (2, "2", ".", ","),
            (2, "2", ",", "."),
            (1234.5, "1.234,5", ",", "."),
            (1234.5, "1,234.5", ".", ","),
            (1234.5, "1234,5", ",", None),
            (1234.5, "1234.5", ".", None),
        ],
    )
    def test_xtoa_converts_number_correctly(self, number, expected_output, decimal_point, thousands_separator):
        result = xtoa(number, decimal_point=decimal_point, thousands_separator=thousands_separator)

        assert result == expected_output

    @pytest.mark.parametrize(
        "new_locale,number,expected_output",
        [
            ("de_CH", 1234.5, "1’234.5"),
            ("de_DE", 1234.5, "1.234,5"),
            ("en_US", 1234.5, "1,234.5"),
            ("nl_NL", 1234.5, "1.234,5"),
            ("zh_CN", 1234.5, "1,234.5"),
        ],
    )
    def test_xtoa_converts_number_correctly_for_different_locale_categories(self, new_locale, number, expected_output):
        if new_locale not in locale.windows_locale.values():
            pytest.skip(f"Locale '{new_locale}' not available.")

        # get new locale
        loc = locale.getlocale()
        locale.setlocale(locale.LC_NUMERIC, new_locale)
        _config.THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
        _config.DECIMAL_POINT = locale.localeconv()["decimal_point"]

        # convert
        result = xtoa(number)

        # restore saved locale
        locale.setlocale(locale.LC_NUMERIC, loc)
        _config.THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
        _config.DECIMAL_POINT = locale.localeconv()["decimal_point"]

        assert result == expected_output

    def test_xtoa_works_correctly_for_opticstudio(self, simple_system):
        deltafocus = 0.5
        steps = 11
        # cfgfile
        fd, cfgoutfile = mkstemp(suffix=".CFG", prefix="zospy_")
        os.close(fd)

        # get analysis
        analysis = new_analysis(simple_system, constants.Analysis.AnalysisIDM.FftThroughFocusMtf)

        # Modify the settings file
        analysis_settings = analysis.GetSettings()
        analysis_settings.SaveTo(cfgoutfile)

        analysis_settings.ModifySettings(cfgoutfile, "TFM_DELTAFOC", xtoa(deltafocus, thousands_separator=None))
        analysis_settings.ModifySettings(cfgoutfile, "TFM_STEPS", xtoa(steps, thousands_separator=None))

        analysis_settings.LoadFrom(cfgoutfile)

        # Run analysis
        analysis.ApplyAndWaitForCompletion()

        os.remove(cfgoutfile)

        assert analysis.Settings.DeltaFocus == deltafocus
        assert analysis.Settings.NumberOfSteps == steps


class TestStringToNumberConversion:
    @pytest.mark.parametrize(
        "string,expected_output,dtype,decimal_point,thousands_separator",
        [
            ("1.5", 1.5, float, ".", ""),
            ("1,5", 1.5, float, ",", ""),
            ("1.5", 1.5, float, ".", ","),
            ("1,5", 1.5, float, ",", "."),
            ("1.5", 1.5, float, ".", None),
            ("1,5", 1.5, float, ",", None),
            ("2", 2, int, ".", ","),
            ("2", 2, int, ",", "."),
            ("1.234,5", 1234.5, float, ",", "."),
            ("1,234.5", 1234.5, float, ".", ","),
        ],
    )
    def test_atox_converts_string_correctly(self, string, expected_output, dtype, decimal_point, thousands_separator):
        result = atox(string, dtype=dtype, thousands_separator=thousands_separator, decimal_point=decimal_point)

        assert isinstance(result, dtype)
        assert result == expected_output

    @pytest.mark.parametrize(
        "string,dtype,thousands_separator,decimal_point",
        [
            ("1,5", float, "", "."),
            ("1.5", int, "", "."),
            ("1,234.5", float, "", "."),
        ],
    )
    def test_atox_raises_error_correctly(self, string, dtype, thousands_separator, decimal_point):
        with pytest.raises(ValueError):
            atox(string, dtype=dtype, thousands_separator=thousands_separator, decimal_point=decimal_point)

    @pytest.mark.parametrize(
        "locale_cat,string,dtype,expected_output",
        [
            ("de_CH", "1’234.5", float, 1234.5),
            ("de_DE", "1.234,5", float, 1234.5),
            ("en_US", "1,234.5", float, 1234.5),
            ("nl_NL", "1.234,5", float, 1234.5),
            ("zh_CN", "1,234.5", float, 1234.5),
            ("de_CH", "1’234", int, 1234),
            ("de_DE", "1.234", int, 1234),
            ("en_US", "1,234", int, 1234),
            ("nl_NL", "1.234", int, 1234),
            ("zh_CN", "1,234", int, 1234),
        ],
    )
    def test_xtoa_converts_string_correctly_for_different_locale_categories(
        self, locale_cat, string, dtype, expected_output
    ):
        if locale_cat not in locale.windows_locale.values():
            pytest.skip(f"Locale '{locale_cat}' not available.")

        # get new locale
        loc = locale.getlocale()
        locale.setlocale(locale.LC_NUMERIC, locale_cat)
        _config.THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
        _config.DECIMAL_POINT = locale.localeconv()["decimal_point"]

        # convert
        result = atox(string, dtype=dtype)

        # restore saved locale
        locale.setlocale(locale.LC_NUMERIC, loc)
        _config.THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
        _config.DECIMAL_POINT = locale.localeconv()["decimal_point"]

        assert result == expected_output

    def test_atox_returns_correct_results_for_opticstudio(self, simple_system):
        xphase = 0.9
        surface = 3

        # cfgfile
        fd, cfgoutfile = mkstemp(suffix=".CFG", prefix="zospy_")
        os.close(fd)

        # txtfile
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)

        analysis = new_analysis(simple_system, constants.Analysis.AnalysisIDM.PolarizationPupilMap)

        # Modify the settings file
        analysis_settings = analysis.GetSettings()
        analysis_settings.SaveTo(cfgoutfile)

        analysis_settings.ModifySettings(cfgoutfile, "PPM_PX", xtoa(xphase, thousands_separator=None))
        if isinstance(surface, str):
            analysis_settings.ModifySettings(cfgoutfile, "PPM_SURFACE", surface)
        else:
            analysis_settings.ModifySettings(cfgoutfile, "PPM_SURFACE", xtoa(surface, thousands_separator=None))

        analysis_settings.LoadFrom(cfgoutfile)

        # Run analysis
        analysis.ApplyAndWaitForCompletion()

        # Get results
        analysis.Results.GetTextFile(txtoutfile)

        with open(txtoutfile, "r", encoding="utf-16-le") as f:
            text_output = f.read()

        xphase_out = atox(_get_number_field("X-Phase", text_output), dtype=float)
        surface_out = atox(_get_number_field("Surface", text_output), dtype=int)

        os.remove(cfgoutfile)
        os.remove(txtoutfile)

        assert isinstance(xphase_out, float)
        assert xphase_out == xphase

        assert isinstance(surface_out, int)
        assert surface_out == surface
