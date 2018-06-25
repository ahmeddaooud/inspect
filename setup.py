#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='PAYFORT Request Inspector',
    version='2.0.0',
    author='PAYFORT',
    author_email='adaoud@payfort.com',
    description='PAYFORT HTTP request collector and inspector',
    packages=find_packages(),
    install_requires=['feedparser'],
    data_files=[],
)
