from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="NQvision",
    version="0.1.0",
    long_description=README,
    long_description_content_type="text/markdown",  # or 'text/x-rst' for reStructuredText
    author="Neuron Q",
    author_email="debbichi1997@gmail.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
