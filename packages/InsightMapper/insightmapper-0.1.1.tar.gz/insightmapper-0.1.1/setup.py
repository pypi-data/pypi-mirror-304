from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="InsightMapper",
    version="0.1.1",
    author="Utkarsh Rana",
    description="A package that maps and visualizes relationships and dependencies between variables in complex datasets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pandas", "numpy", "scikit-learn", "networkx", "matplotlib"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
