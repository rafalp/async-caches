#! /usr/bin/env python
import os
from setuptools import setup

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
with open(README_PATH, "r") as f:
    README = f.read()

setup(
    name="caches",
    author="Rafał Pitoń",
    author_email="kontakt@rpiton",
    description="Async caching library inspired by django.core.caches.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="BSD",
    version="0.1.0",
    url="https://github.com/rafalp/caches",
    packages=["caches"],
    include_package_data=True,
    install_requires=["aioredis>=1.2.0"],
    classifiers=CLASSIFIERS,
    platforms=["any"],
    zip_safe=False,
)