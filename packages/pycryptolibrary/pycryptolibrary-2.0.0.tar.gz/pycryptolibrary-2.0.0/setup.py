from setuptools import setup, find_packages

VERSION = '2.0.0'
DESCRIPTION = "Python Library for cryptography"
LONG_DESCRIPTION = "Python Library for cryptography"

# Setting up
setup(
    name="pycryptolibrary",
    version=VERSION,
    author="SuSB0t",
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