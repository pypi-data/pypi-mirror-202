from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.52'
DESCRIPTION = 'Arithmatic Library for Quick Calculations'

# Setting up
setup(
    name="simple-arith",
    version=VERSION,
    author="Durgesh Kavate",
    author_email="<durgeshkavate7128@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'calculation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)