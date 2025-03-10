from pathlib import Path

# Reference version of OpticStudio, with which all analysis outputs are compared
REFERENCE_VERSION: str = "25.1.1"

# Folder with configuration files for tests of *_fromcfg analyses
CONFIG_DATA_FOLDER: Path = Path("tests/data/config")

# Folder with reference data for analyses
REFERENCE_DATA_FOLDER: Path = Path("tests/data/reference")
