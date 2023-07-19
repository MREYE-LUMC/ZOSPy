<!--
  Thanks a lot for contributing to our project!
  Please, do not remove any text from this template (unless instructed otherwise).
-->
## Proposed change
<!--
  What did you change and why did you change it?
-->

## Type of change
<!--
  What type of change does your PR introduce to ZOSPy?
-->

- [ ] Example (a notebook demonstrating how to use ZOSPy for a specific application)
- [ ] Bugfix (non-breaking change which fixes an issue)
- [ ] New analysis (a wrapper around an OpticStudio analysis)
- [ ] New feature (other than an analysis)
- [ ] Breaking change (fix/feature causing existing functionality to break)
- [ ] Code quality improvements to existing code or addition of tests

# Additional information
<!--
  We would like to know which versions of Python and OpticStudio you are running.
  This helps us to keep the compatibility section in our documentation updated.
  
  Please list all Python versions you used to test your changes. The unit tests will
  automatically try to test all currently supported Python versions. If you would like
  to do us a favor, install all necessary Python versions on your system. This helps
  us to ensure compatibility and detect any problems we might not be able to detect
  on our own systems. This makes your contribution even more valuable!
-->

- Python version: ...
- OpticStudio version: ...

## Related issues
<!--
  Please list any issues, discussions or pull requests related to this pull request.
-->

## Checklist
<!--
  Tick all boxes that apply. 
-->

- [ ] I have followed the [contribution guidelines][contribution-guidelines]
- [ ] The code has been linted, formatted and tested locally using tox.
- [ ] Local tests pass. **Please fix any problems before opening a PR. If this is not possible, specify what doesn't work and why you can't fix it.**
- [ ] I added new tests for any features contributed, or updated existing tests.
- [ ] I updated CHANGELOG.md with my changes (except for refactorings and changes in the documentation).

If you contributed an analysis:

- [ ] I did not use `AttrDict`s for the analysis result data (please use dataclasses instead).

If you contributed an example:

- [ ] I contributed my example as a Jupyter notebook.
<!--
  This is important, because it allows users to see the results without
  executing the complete example.
-->

<!--
  Thanks again for your contribution! We will look into it soon.
  Meanwhile, here are some useful resources that will help you to improve
  the quality of your contribution:
-->
[contribution-guidelines]: https://github.com/MREYE-LUMC/ZOSPy/blob/main/CONTRIBUTING.md
[unittest-instructions]: https://github.com/MREYE-LUMC/ZOSPy/blob/main/tests/README.md
[numpydoc]: https://numpydoc.readthedocs.io/en/latest/format.html
