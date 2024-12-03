from setuptools import setup, find_packages

setup(
    name="ieee_papers_mapper",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
