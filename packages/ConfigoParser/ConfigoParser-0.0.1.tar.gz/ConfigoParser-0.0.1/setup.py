from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Parser For Configuration File'
LONG_DESCRIPTION = 'Helps to Import data from configuration file'

# Setting up
setup(
    name="ConfigoParser",
    version=VERSION,
    author="programmingrakesh",
    author_email="subburakesh2255@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
