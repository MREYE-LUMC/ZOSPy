from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ZOSPy',
    version='0.5',
    packages=['zospy', 'zospy.api', 'zospy.analyses', 'zospy.functions', 'zospy.utils'],
    url='https://git.lumc.nl/ophthalmology/virtualeyemodelling/zospy',
    license='CC0 1.0 Universal',
    author='Luc van Vught, Jan-Willem Beenakker',
    description="A Python package used to communicate with Zemax OpticStudio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='l.van_vught@lumc.nl',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
            ],
    python_requires='>=3.0', install_requires=['pythonnet', 'pandas', 'numpy'],
    include_package_data=True
)
