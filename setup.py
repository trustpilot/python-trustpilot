#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys
import os

readme = open("README.md", "r").read()

history = open("HISTORY.md").read()

requirements = ["Click==6.7", "requests>=2.20.0"]

test_requirements = [
    "responses==0.6",
    "mock",
    "pytest==3.2.0",
    "pytest-readme==1.0.0",
] + requirements

if sys.version_info >= (3, 5):
    test_requirements.append("aioresponses==0.3.1")

async_requirements = ["aiohttp==2.3.9"] + requirements

extras = {"test": test_requirements, "async": async_requirements}
# get version
metadata = {}
version_filename = os.path.join(os.path.dirname(__file__), "trustpilot", "__init__.py")
exec(open(version_filename).read(), None, metadata)

setup(
    name="trustpilot",
    version=metadata["__version__"],
    description="trustpilot api client including cli tool",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author=metadata["__author__"],
    author_email=metadata["__email__"],
    url="https://github.com/trustpilot/python-trustpilot",
    packages=["trustpilot"],
    package_dir={"trustpilot": "trustpilot"},
    entry_points={"console_scripts": ["trustpilot_api_client=trustpilot.cli:cli"]},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="trustpilot api client",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    extras_require=extras,
)
