from setuptools import setup
from setuptools_scm import get_version

version = "0.0.0"  # get_version(root="../..")

setup(
    version=version,
    install_requires=[
        f"toga-core == {version}",
    ],
)
