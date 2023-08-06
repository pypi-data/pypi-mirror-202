from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A basic machine learning package'

setup(
    name="obeenya",
    version=VERSION,
    author="Benjamin Aubignat",
    author_email="<benjamin.aubignat@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
)
