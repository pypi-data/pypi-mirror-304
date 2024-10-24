#!/usr/bin/env python3

from setuptools import setup, find_packages
import os


def get_version():
    """Get version from git or version file"""
    version = "0.0.0"  # Default version

    # Try to get version from VERSION file (created by CI)
    if os.path.exists('VERSION'):
        with open('VERSION', 'r') as f:
            version = f.read().strip()

    return version


setup(
    name="openapi_qase_suite_generator",
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "PyYAML>=6.0.1"
    ],
    entry_points={
        "console_scripts": [
            "openapi_qase_suite_generator=openapi_qase_suite_generator:main"
        ]
    },
    author="Petra Barus",
    author_email="petra.barus@gmail.com",
    description="Generate Qase test suites from OpenAPI specs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="qase openapi testsuite",
    url="https://github.com/petrabarus/openapi_qase_suite_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9"
)
