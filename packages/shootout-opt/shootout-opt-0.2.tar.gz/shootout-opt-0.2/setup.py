#!/usr/bin/env python

import setuptools
import os

# Installing packages in requirements
thisfolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thisfolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


setuptools.setup(
      name='shootout-opt',
      version='0.2',
      description='Run algorithms, store and compare their outputs',
      author='Jeremy E. Cohen',
      author_email='jeremy.cohen@cnrs.fr',
      license='MIT',
      install_requires=install_requires
     )