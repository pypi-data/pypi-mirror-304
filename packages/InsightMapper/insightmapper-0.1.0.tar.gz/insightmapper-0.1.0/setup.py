from setuptools import setup, find_packages

setup(
    name="InsightMapper",
    version="0.1.0",
    author="Utkarsh Rana",
    description="A package that maps and visualizes relationships and dependencies between variables in complex datasets.",
    packages=find_packages(),
    install_requires=["pandas", "numpy", "scikit-learn", "networkx", "matplotlib"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
