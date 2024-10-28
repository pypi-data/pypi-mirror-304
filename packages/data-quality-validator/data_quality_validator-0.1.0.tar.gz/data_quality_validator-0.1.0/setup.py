# setup.py

from setuptools import setup, find_packages

setup(
    name="data_quality_validator",
    version="0.1.0",
    author="Pooja Sambhwani",
    author_email="sambhwanipooja08@example.com",
    description="A package for validating data quality",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/poojasambhwani/data_quality_validator",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "pandas-profiling"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
