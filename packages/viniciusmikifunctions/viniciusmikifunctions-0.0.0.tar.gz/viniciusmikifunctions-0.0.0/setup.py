from setuptools import setup, find_packages
import codecs
import os

VERSION = ''
DESCRIPTION = 'This is a package with some helpful functions =D'


# Setting up
setup(
    name="viniciusmikifunctions",
    version=VERSION,
    author="Vinicius Miki",
    author_email="<vinicius_miki@hotmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)