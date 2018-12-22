#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

# import sys
# import sectw.builder
# from setuptools.command.install import install


# class sectw_installer(install):
#
#     def run(self):
#         print('Building newest section data ... ')
#         sys.stdout.flush()
#         sectw.builder.build()
#         install.run(self)


import sectw
from setuptools import setup, find_packages

setup(

    name='sectw',
    version=sectw.__version__,
    description='Find land section code in Taiwan by address fuzzily.',
    long_description='Find land section code in Taiwan by address fuzzily.',
    author='ssivart',
    url='https://github.com/ssivart/sectw',
    author_email='travishen.tw@gmail.com',
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages=find_packages(),
    install_requires=['sqlalchemy', 'regex', 'six', 'requests'],
    package_data={'sectw': ['*.csv']},

    # cmdclass={'install': sectw_installer},
)
