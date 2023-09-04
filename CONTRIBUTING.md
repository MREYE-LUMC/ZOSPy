# Contributing to ZOSPy

Thank you for considering contributing to ZOSPy! Before contributing, please read these guidelines, so we can process
your contribution as quickly as possible.

## Contribution ideas

ZOSPy aims to make interaction between Python and Zemax/Ansys OpticStudio as easy as possible by providing a Pythonic
interface for the OpticStudio API.
Any contributions serving this goal, or aiding optical simulations in OpticStudio, are welcome. If you don't know what to contribute, here are some ideas that are
definitely welcome:

1. Examples of various kinds of optical systems (in `examples/`). These can be supplied as Python scripts, but Jupyter
   Notebooks are preferred;
2. Implementation of additional analyses (in `zospy/analyses`). Please refer to other analyses on how to implement them.
   If you add a new
   analysis, please include unit tests as well;
3. Implementation of additional solvers (in `zospy/solvers`);
4. Compatibility checks. If you are using a version of OpticStudio that is not listed in the [README](README.md),
   please [run the unit tests](#3-test) and update the README accordingly.

## Code style

- Please format your docstrings according to [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html).
- Additional code styling is automatically applied when running the tests using `tox`.

## Workflow

### 1. Setting up a development environment

For development, additional dependencies are necessary for unit testing etc. They can be installed by running

```shell
pip install .[dev]
```

in the project directory.

### 2. Add your new feature

Add your contribution in a new feature branch. When contributing an analysis, please include unit tests.

### 3. Test

Since automated testing using GitHub Actions is not possible due to the dependency on OpticStudio, we request you
to run all unit tests prior to opening a Pull Request. Testing has been automated for multiple Python versions and
can be initiated by running

```shell
tox
```

in the project directory. More information about running the unit tests can be found [here](tests/README.md).
If you run the tests for a previously untested version of OpticStudio or added tests for analysis wrappers, 
do not forget to generate reference data for these tests.
More information about this can be found in [the test documentation](tests/README.md#generating-test-reference-data).

### 4. Open a Pull Request

Open a Pull Request, wait for our suggestions, and get your contribution merged!
