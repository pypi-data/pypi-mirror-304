from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'This is just for test'
LONG_DESCRIPTION = 'Python package is just for test'

# Setting up
setup(
    name="akh-py",
    version=VERSION,
    author="Abir",
    author_email="hide66501x@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'discord'],
    keywords=[]
   )
