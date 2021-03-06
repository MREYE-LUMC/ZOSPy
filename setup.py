from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='zospy',
    version='0.5.1',
    packages=['zospy'] + ['zospy.' + ii for ii in find_namespace_packages(where='zospy')],
    url='https://github.com/MREYE-LUMC/ZOSPy',
    license='CC0 1.0 Universal',
    author='Luc van Vught, Jan-Willem Beenakker',
    author_email='l.van_vught@lumc.nl',
    description="A Python package used to communicate with Zemax OpticStudio through the API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['Zemax', 'OpticStudio', 'API'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
            ],
    python_requires='>=3.0', install_requires=['pythonnet', 'pandas', 'numpy'],
    include_package_data=True
)
