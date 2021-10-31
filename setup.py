# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ObjectCounter',
    version='0.1.0',
    description='Count Objects in Images',
    long_description=readme,
    author='Stefan Knaak',
    author_email='stefan@knaak.org',
    url='https://github.com/corgan2222/E-Shelter_ObjectCount',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)    
