#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="test-mqc-core",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "click",
    ],
    extras_require = {
        'all':  ["test-mqc-module"]
    }
)

print(
    """
--------------------------------
 MultiQC installation complete!
--------------------------------
For help in running MultiQC, please see the documentation available
at http://multiqc.info or run: multiqc --help
"""
)
