# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ZOSPy"
copyright = "2023, Jan-Willem M. Beenakker, Luc van Vught, Corné Haasjes"
author = "Jan-Willem M. Beenakker, Luc van Vught, Corné Haasjes"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # "autodoc2",
    "myst_parser",
    "nbsphinx",
    "nbsphinx_link",
    "numpydoc",
    # "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx_design",
]

myst_enable_extensions = ["colon_fence", "attrs_block"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_theme_options = {"home_page_in_toc": True}


# -- Options for Sphinx autodoc and numpydoc ---------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
# https://numpydoc.readthedocs.io/en/latest/install.html

# Display type hints in short form and only in the signature
autodoc_typehints = "signature"
autodoc_class_signature = "separated"
autodoc_typehints_format = "short"

# Mock imports that may be unavailable in the build environment (e.g. readthedocs)
autodoc_mock_imports = ["winreg", "clr", "System"]

numpydoc_class_members_toctree = False

# Do not document inherited class members for these types, e.g. because they extend built-in Python types
numpydoc_show_inherited_class_members = {
    "zospy.analyses.base.AttrDict": False,
    "zospy.analyses.base.AnalysisResult": False,
    "zospy.analyses.base.OnComplete": False,
}


# -- Docstring preprocessing -------------------------------------------------
ANNOTATION_SUBSTITUTIONS = {"_ZOSAPI": "ZOSAPI"}


def apply_annotation_substitutions(app, obj: object, bound_method):
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
