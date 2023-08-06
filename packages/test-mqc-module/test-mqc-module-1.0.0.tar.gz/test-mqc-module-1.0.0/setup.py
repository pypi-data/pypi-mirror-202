#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="test-mqc-module",
    version='1.0.0',
    description="MultiQC module",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "test-mqc-core",
    ],
)
