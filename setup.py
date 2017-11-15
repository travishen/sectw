#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='sectw',
    packages=['sectw'],
    license='MIT',
    version='1.0',
    description='Find land code in Taiwan by address progressively and fuzzily',
    author='ssivart',
    author_email='travishen.tw@gmail.com',
    url='https://github.com/travishen/sectw',
    download_url='https://github.com/travishen/sectw/releases/tag/v1.0',
    keywords=['taiwan', 'land-section-code'],
    install_requires=['sqlalchemy', 'regex', 'six'],
    classifiers=[],
)
