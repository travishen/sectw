#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='sectw',
    packages=['sectw', 'database'],
    license='MIT',
    version='1.0',
    description='Find land code in Taiwan by address and create local DB.',
    author='ssivart',
    author_email='travishen.tw@gmail.com',
    url='https://github.com/travishen/sectw',
    download_url='https://github.com/travishen/sectw/releases/tag/v1.0',
    keywords=['taiwan', 'landsectioncode'],
    install_requires=['sqlalchemy', 'regex'],
    classifiers=[],
)
