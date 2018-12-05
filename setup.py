# coding: utf-8
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from setuptools import setup, find_packages

setup(
    name = "Meli-App-Server",
    version = "1.0.0",
    author = "Estanislao Ledesma",
    author_email = "estanislaomledesma@gmail.com",
    description = ("App server para la aplicación Meli"),
    license = "BSD",
    keywords = "meli app server",
    url = "http://meli-",
    packages=find_packages(),
    long_description= read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)