#!/usr/bin/env python3

from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent

setup(
    name="earthquakepy",
    version="0.3.10",
    description="python library for earthquake engineers.",
    long_description = (this_directory / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/gauthamrdy/earthquakepy",
    author="Gautham Reddy, Digvijay Patankar",
    author_email="pgrddy@gmail.com, dbpatankar@gmail.com",
    license="GNU GPLv3",
    packages=["earthquakepy"],
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
