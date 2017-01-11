#!/usr/bin/env python

from __future__ import print_function

from setuptools import setup, find_packages

entry_points = """
[glue.plugins]
h5part=glue_h5part:setup
"""

with open('README.rst') as readme:
    LONG_DESCRIPTION = readme.read()

from glue_h5part import __version__

setup(name='glue-h5part',
      version=__version__,
      description='Experimental plugin to read in and explore h5part files',
      long_description=LONG_DESCRIPTION,
      url="https://github.com/glue-viz/glue-h5part",
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      packages = find_packages(),
      package_data={},
      entry_points=entry_points
    )
