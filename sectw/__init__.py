#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import dirname, join
from .database.config import setup_session
from .util import Directory

# paths
_package_root = dirname(__file__)
_csv_version = '2017-11-06'
_csv_path = join(_package_root, '{}.csv'.format(_csv_version))

# create a instance
_dir = Directory(_csv_path)

# expose function
find = _dir.find
