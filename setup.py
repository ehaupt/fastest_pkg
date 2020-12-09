import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "fastest_pkg",
    version = "0.1.3",
    author = "Emanuel Haupt",
    author_email = "ehaupt@FreeBSD.org",
    description = ("Script to find the fastest FreeBSD.org pkg mirror."),
    license = "BSD",
    keywords = "FreeBSD fastest pkg mirror",
    url = "https://github.com/ehaupt/fastest_pkg",
    install_requires=required,
    scripts=[
        'fastest_pkg',
    ],
    long_description=read('README.md'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
