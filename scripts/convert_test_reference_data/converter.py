from __future__ import annotations

from operator import attrgetter
from string import Template
from typing import Callable, Literal

from jsonata import Jsonata

import zospy as zp


class JSONataExpressionTemplate(Template):
    delimiter = "%"


class DataConversion:
    DEFAULT = "$.data.Data.data"
    DATAFRAME = DEFAULT


class SettingsConversion:
    DEFAULT = "$each($.data.Settings.data, function($v, $k) {{ $camelToSnake($k): $v}}) ~> $merge"


class ConversionExpression(Jsonata):
    EXPRESSION = JSONataExpressionTemplate(r"""
(
    /* Convert CamelCase variables to snake_case */
    $camelToSnake := function($s) {(
        /* Split groups and separate with underscore */
        $snake := $replace($s, /(?<!^)((?<=[a-z])[A-Z]|[A-Z](?=[a-z])|(?<=[A-Z])[0-9])/, "_$1").$lowercase();
        /* Remove dashes, spaces, and make lowercase */
        $snake.$replace(/[\(\)]/, "").$replace(/[\-\s]/, "_").$replace(/_+/, "_")
    )};

    {
        "data": %data,
        "settings": %settings,
        "metadata": $each($.data.MetaData.data, function($v, $k){
            { $k: $v.data ? $v.data : $v }
        }) ~> $merge,
        "header": $.data.HeaderData,
        "messages": $.data.Messages
    };
)
""")

    def __init__(self, *, data=DataConversion.DEFAULT, settings=SettingsConversion.DEFAULT):
        super().__init__(self.EXPRESSION.substitute(data=data, settings=settings))


class AnalysisDataConverter:
    def __init__(
        self,
        old_analysis: str,
        new_analysis: str,
        settings_class: str,
        module: str,
        data_type: Literal["dataframe", "dataclass"],
        data_class: str | None = None,
        data_conversion: str = DataConversion.DEFAULT,
        settings_conversion: str = SettingsConversion.DEFAULT,
        settings_replace_keys: dict[str, str] | None = None,
        settings_convert_constants: dict[str, str] | None = None,
        postprocess: Callable[[dict], None] | None = None,
    ):
        """Initialize a converter for analysis data.

        Parameters
        ----------
        old_analysis : str
            The name of the old analysis.
        new_analysis : str
            The name of the new analysis.
        settings_class : str
            The name of the settings class.
        module : str
            The module where the settings class is defined.
        data_type : Literal["dataframe"]
            The type of the data.
        data_conversion : str, optional
            The JSONata expression to convert the data, by default returns the data as is.
        settings_replace_keys : dict[str, str], optional
            A dictionary to replace keys in the settings, by default None. Should be in the form {old_key: new_key}.
            This can be used to rename keys in the settings to match the new analysis, in case the conversion to
            snake_case does not result in the correct key.
        settings_convert_constants : list[str], optional
            A mapping of settings keys to constants that need to be converted from an integer to a string.
            Should be in the form {key: constant_name}.
        """
        if data_type == "dataclass" and data_class is None:
            raise ValueError("data_class is required for data_type 'dataclass'")

        self.old_analysis = old_analysis
        self.new_analysis = new_analysis
        self.settings_class = settings_class
        self.module = module
        self.data_type = data_type
        self.data_class = data_class
        self.data_conversion = data_conversion
        self.settings_conversion = settings_conversion
        self.settings_replace_keys = settings_replace_keys
        self.settings_convert_constants = settings_convert_constants
        self.postprocess = postprocess

    def add_metadata(self, data: dict):
        metadata = {
            "__analysis_data__": {
                "data_type": self.data_type,
            },
            "__analysis_settings__": {
                "data_type": "dataclass",
                "name": self.settings_class,
                "module": self.module,
            },
        }

        if self.data_type == "dataclass":
            metadata["__analysis_data__"]["name"] = self.data_class
            metadata["__analysis_data__"]["module"] = self.module

        data.update(metadata)

    def replace_settings_keys(self, settings: dict):
        if self.settings_replace_keys is not None:
            for old_key, new_key in self.settings_replace_keys.items():
                if old_key in settings:
                    settings[new_key] = settings.pop(old_key)

    def convert_settings_constants(self, settings: dict | None):
        if self.settings_convert_constants is not None and settings is not None:
            zos = zp.ZOS()  # noqa: F841

            for key, constant in self.settings_convert_constants.items():
                zospy_constant = attrgetter(constant)(zp.constants)

                try:
                    settings[key] = zp.constants.get_constantname_by_value(zospy_constant, int(settings[key]))
                except ValueError as e:
                    print(f"Error converting constant {key}: {e}")

    def convert_data(self, data: dict):
        converter = ConversionExpression(data=self.data_conversion, settings=self.settings_conversion)
        converted_data = converter.evaluate(data)
        self.replace_settings_keys(converted_data["settings"])
        # self.convert_settings_constants(converted_data["settings"])
        self.add_metadata(converted_data)

        if self.postprocess is not None:
            self.postprocess(converted_data)

        return converted_data
