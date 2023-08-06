from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'A 2D game engine for python that is incredibly easy to use and that has a many tools.'
LONG_DESCRIPTION = 'A 2D game engine for python that is incredibly easy to use and that has a many tools made in pygame.'

# Setting up
setup(
    name="pyspal",
    version=VERSION,
    author="Perfogy",
    author_email="<perfogyofficial@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'game engine', '2d', 'games', 'game', 'perfogy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)