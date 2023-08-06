from setuptools import setup, find_packages

VERSION = '1.2.0'
DESCRIPTION = "Package that helps with crypto libarys"
LONG_DESCRIPTION = "Package that helps with crypto libarys"

# Setting up
setup(
    name="cryptolibs",
    version=VERSION,
    author="NHJonas",
    author_email="nick.faltermeier@gmx.de",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)