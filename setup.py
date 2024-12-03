#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="ieee_papers_mapper",
    version="1.0.0",
    author="Alexandros Anastasiou",
    author_email="anastasioyaa@gmail.com",
    description="A project for fetching, processing, and classifying IEEE papers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alex-anast/ieee-papers-mapper",
    packages=find_packages(where="ieee_papers_mapper"),
    package_dir={"": "ieee_papers_mapper"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Ubuntu :: 24.04",
    ],
    python_requires=">=3.12",
    # List only the parent packages needed, not their dependencies as well
    # It is not the same as `requirements.txt` !!!
    install_requires=[
        "pandas",
    ],
)
