# -*- coding: utf-8 -*-
"""
setup.py

python-can-canine
"""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="python-can-slcan_disco",
    version="0.1.0",
    author="Yannis Chatzikonstantinou",
    author_email="info@tinymovr.com",
    description="Python-can slcan driver with discovery",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yconst/python-can-slcan_disco",
    py_modules = ["slcan_disco"],
    python_requires=">=3.9",
    install_requires=[
        "python-can"
        ],
    entry_points = {
        'can.interface': [
            'slcan_disco = slcan_disco:slcanDiscoBus'
        ]
    }
)
