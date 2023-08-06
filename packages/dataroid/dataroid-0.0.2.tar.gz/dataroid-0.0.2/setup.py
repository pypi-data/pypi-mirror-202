from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'A Simple Wrapper For Synthetic Data Generation'

# Setting up
setup(
    name="dataroid",
    version=VERSION,
    author="torchd3v (Burak Egeli)",
    author_email="<burak96egeli@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas==1.5.3', 'ctgan==0.7.1'],
    keywords=['python', 'data', 'generate', 'synthetic', 'deep learning', 'model'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)