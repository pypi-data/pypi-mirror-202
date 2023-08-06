from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Simple Wrapper For Synthetic Data Generation'

# Setting up
setup(
    name="dataroid",
    version=VERSION,
    author="torchd3v (Burak Egeli)",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'ctgan'],
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