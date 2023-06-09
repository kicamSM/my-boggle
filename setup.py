import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="boggle",
    version="0.0.1",
    author="Sophia Macik",
    author_email="kicamSMM@gmail.com",
    description=("Is Boggle"),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/",

    packages=find_packages(),
)
