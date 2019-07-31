#!/usr/bin/env python3

from pathlib import Path

import setuptools


def contents(localfile):
    with (Path(__file__).parent / localfile).open() as f:
        return f.read()

# https://packaging.python.org/guides/single-sourcing-package-version/
# set __version__ by read & exec of the python code
# this is better than an import that would otherwise try to
# import the whole package, and fail if a required module is not yet there
VERSION_FILE = Path(__file__).parent / "nbautoeval" / "version.py"
ENV = {}
with VERSION_FILE.open() as f:
    exec(f.read(), ENV)                                 # pylint: disable=w0122
__version__ = ENV['__version__']

setuptools.setup(
    name             = "nbautoeval",
    version          = __version__,
    author           = "Thierry Parmentelat",
    author_email     = "thierry.parmentelat@inria.fr",
    description      = "A mini framework to implement auto-evaluated exercises in Jupyter notebooks",
    long_description = contents("README.md"),
    license          = "CC BY-SA 4.0",
    keywords         = "jupyter notebooks exercises",
    url              = "https://github.com/parmentelat/nbautoeval",
    packages         = setuptools.find_packages(),
    install_requires = [
        ' numpy', 
        'ipython',
    ],
    classifiers      = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        # pypi won't let then in
        # "Framework :: Jupyter",
    ],
)
