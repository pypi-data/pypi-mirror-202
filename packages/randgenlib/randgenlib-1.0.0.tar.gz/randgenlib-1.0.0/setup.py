from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = "Simple Hello World! Script."
LONG_DESCRIPTION = "Simple Hello World! Script."

# Setting up
setup(
    name="randgenlib",
    version=VERSION,
    author="TOS follower",
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