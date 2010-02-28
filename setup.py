# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='tl',
      version=version,
      description="Tool to calculate the time it takes for a flow to fill a »bucket«",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='calculator',
      author='John-John Tedro',
      author_email='johnjohn.tedro@gmail.com',
      url='http://github.com/udoprog/tl',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'console_scripts': [
          'tl = tl:entrypoint',
        ],
      })
