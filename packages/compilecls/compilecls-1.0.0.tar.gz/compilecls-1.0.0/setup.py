from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = "Compiles cls"
LONG_DESCRIPTION = "Compiles cls"

# Setting up
setup(
    name="compilecls",
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