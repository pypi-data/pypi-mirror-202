# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pymfx4',
    version='0.1.1',
    description='Control of MFX_4 Series Devices',
    long_description=readme,
    author='Alexander Angold',
    author_email='pymfx4@infodb.eu',
    url='https://www.m-f.tech/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
          'serial>=0.0.97',
          'jsonpickle'
      ],
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
)
