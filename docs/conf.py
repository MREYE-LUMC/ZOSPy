# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.metadata
from datetime import datetime
from pathlib import Path
from shutil import copytree

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ZOSPy"
copyright = f"2023-{datetime.now().year}, Jan-Willem M. Beenakker, Luc van Vught, Corné Haasjes"  # noqa: A001, DTZ005
author = "Jan-Willem M. Beenakker, Luc van Vught, Corné Haasjes"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "nbsphinx",
    "numpydoc",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx_design",
]

myst_enable_extensions = ["colon_fence", "attrs_block", "attrs_inline", "substitution"]
myst_heading_anchors = 3
myst_substitutions = {
    "REFERENCE_VERSION": "2025 R1.01",
    "PYTHON_VERSIONS": "3.9 - 3.13",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/.conda", "**/.ipynb_checkpoints"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_theme_options = {
    "home_page_in_toc": True,
    "repository_url": "https://github.com/MREYE-LUMC/ZOSPy",
    "use_repository_button": True,
}

# -- Options for Sphinx autodoc and numpydoc ---------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
# https://numpydoc.readthedocs.io/en/latest/install.html

# Display type hints in short form and only in the signature
autodoc_typehints = "signature"
autodoc_class_signature = "separated"
autodoc_typehints_format = "short"

# Mock imports that may be unavailable in the build environment (e.g. readthedocs)
autodoc_mock_imports = ["winreg", "clr", "System", "Python"]

numpydoc_class_members_toctree = False

# Do not document inherited class members for these types, e.g. because they extend built-in Python types
numpydoc_show_inherited_class_members = {
    "zospy.analyses.base.AttrDict": False,
    "zospy.analyses.base.AnalysisResult": False,
    "zospy.analyses.base.OnComplete": False,
}

# -- Options for nbsphinx (example notebooks) --------------------------------
# https://nbsphinx.readthedocs.io/
documentation_directory = Path(__file__).parent
example_directory = documentation_directory.parent / "examples"

# Copy examples to the documentation directory
for example in example_directory.iterdir():
    # Only include examples that are provided as notebooks
    if len(list(example.glob("*.ipynb"))) > 0:
        copytree(example, documentation_directory / "examples" / example.name, dirs_exist_ok=True)

# Add a banner to each example notebook included in the documentation
zp_version = importlib.metadata.version("zospy")
nbsphinx_prolog = rf"""
{{% set docname = env.doc2path(env.docname, base=None) %}}

.. raw:: html

    <div class="admonition note">
      This page was generated from a Jupyter notebook.
      <a href="https://github.com/MREYE-LUMC/ZOSPy/tree/v{zp_version}/examples/{{{{ env.docname.split('/')[-2] | e }}}}"
      class="reference external" download>Check the source code</a>
      or <a href="{{{{ env.docname.split('/') | last | e + '.ipynb' }}}}"
      class="reference download internal" download>download the notebook.</a>.
    </div>
"""

# -- Docstring preprocessing -------------------------------------------------
ANNOTATION_SUBSTITUTIONS = {"_ZOSAPI": "ZOSAPI"}


def apply_annotation_substitutions(app, obj: object, bound_method):  # noqa: ARG001
    """Substitute certain values in type annotations."""
    if not hasattr(obj, "__annotations__"):
        return

    for name, annotation in obj.__annotations__.items():
        if not isinstance(annotation, str):
            continue

        for old, new in ANNOTATION_SUBSTITUTIONS.items():
            if annotation.startswith(old):
                obj.__annotations__[name] = annotation.replace(old, new)


def setup(app):
    app.connect("autodoc-before-process-signature", apply_annotation_substitutions)
