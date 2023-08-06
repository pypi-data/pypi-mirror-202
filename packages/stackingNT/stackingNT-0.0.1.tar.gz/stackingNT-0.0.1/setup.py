import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "3.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '0.0.1'
DESCRIPTION = 'Stacking algorithm optimisation'
LONG_DESCRIPTION = 'Stacking algorithm optimisation'

# Setting up
setup(
    name="stackingNT",
    version=VERSION,
    author="caoxinyu",
    author_email="398424191@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'menu', 'dumb_menu','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)