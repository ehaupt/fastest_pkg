import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="fastest_pkg",
    version="0.2.1",
    author="Emanuel Haupt",
    author_email="ehaupt@FreeBSD.org",
    description=("Script to find the fastest FreeBSD.org pkg mirror."),
    license="BSD",
    keywords="FreeBSD fastest pkg mirror",
    url="https://github.com/ehaupt/fastest_pkg",
    install_requires=required,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fastest_pkg = fastest_pkg.fastest_pkg:main",
        ],
    },
    long_description=read("README.md"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
