# Unit tests for ZOSPy

ZOSPy uses [PyTest](https://docs.pytest.org) for unit testing. [Tox](https://tox.wiki) is used to automate testing for
different Python versions, and to run tests in an isolated environment. Running the tests with tox also ensures that the
package can be properly installed.

## How to run

- Install [tox](https://tox.wiki):
  ```shell
  pip install tox
  ```
- Run all tests:
  ```shell
  tox run
  ```
- Alternatively, only selected test environments can be run:
  ```shell
  # Run only on Python 3.10 in extension mode and 3.11 in standalone mode
  tox run -e py310-extension,py311-standalone
  
  # Run environments with label "test-standalone" only
  tox run -m test-standalone
  ```
- When running tests in extension mode, first open Zemax OpticStudio, enable the Interactive Extension mode, and
  uncheck "Auto Close on Disconnect".

## Command line options

- **`--extension`**: Since the ZOS-API is limited to only a single connection per session, it is not possible to test
  ZOSPy in extension mode and standalone mode simultaneously. Specifying the command line flag `--extension` instructs
  PyTest to connect to Zemax OpticStudio in extension mode. Make sure the interactive extension mode has been activated
  and `Auto Close on Disconnect` is unchecked.
- **`--output-directory=<OUTPUT_DIRECTORY>`**: If specified, all created OpticStudio systems are saved to this
  directory.

These arguments can also be passed to tox, e.g. (note the double dashes `--` after the tox arguments):

```shell
tox run -e py311-standalone -- --output-directory="zospy/is/cool" 
```