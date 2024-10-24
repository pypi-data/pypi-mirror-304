#!/usr/bin/env python3

from setuptools import setup, find_packages
import os


def get_version():
    import os
    
    # Try to get version from environment variable
    version = os.environ.get('PACKAGE_VERSION', '0.0.0')
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
