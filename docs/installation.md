# Installation

ZOSPy is available through [PyPI](https://pypi.org/project/zospy/) and [conda-forge](https://anaconda.org/conda-forge/zospy).


::::{tab-set}
:::{tab-item} Installing via pip
To install ZOSPy via pip, run the following command in your terminal:

```bash
pip install zospy
```
:::
:::{tab-item} Installing via conda
To install ZOSPy via conda, run the following command in your terminal:

```bash
conda install conda-forge::zospy
```
:::
::::

## Using ZOSPy in a separate environment

We recommend to use ZOSPy in a separate (virtual) environment to prevent conflicts with other packages or older
ZOS-API projects.

:::::{tab-set}
::::{tab-item} Using conda
To create a new conda environment named 'optics', with Python 3.12 and ZOSPy installed, run the following commands:

```bash
conda create -n optics -c conda-forge python=3.12 zospy
```
::::
::::{tab-item} Using venv
To create a new virtual environment named 'zospy_venv', with ZOSPy installed, run the following commands:

```bash
# Create a new virtual environment
python -m venv zospy_venv

# Activate the virtual environment
.\zospy_venv\Scripts\activate

# Install ZOSPy in the virtual environment
pip install zospy
```

:::{note}
Although the `venv` module is included in the Python standard library, there are many environment management tools available
that are easier to use, such as [virtualenv](https://virtualenv.pypa.io/en/latest/), [uv](https://docs.astral.sh/uv/),
[pipenv](https://pipenv.pypa.io/en/latest/), and [poetry](https://python-poetry.org/).
We recommend using one of these tools for managing your virtual environments.
:::
::::
:::::
