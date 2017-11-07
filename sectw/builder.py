#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import logging
import argparse
from . import api
from .database import model, config
import json
import datetime


def build():
    try:
        version = api.collect()
        data = json.dumps(version, cls=model.ORMEncoder)
        csv_version = version.date
        with open('sectw\{}.csv'.format(csv_version), 'w') as file:
            file.write(data)
        print('Version added to folder. If you want to use newer version, please edit __init__.py in the package.')
    except:
        logging.exception('message')


def build_cmd(db_path=None, setup=False):
    today = datetime.date.today()
    try:
        config.setup_session(db_path)
        if setup:
            config.init()
        with config.session_scope() as session:
            latest_version = model.Version.get_latest_version(session)
            if latest_version is not None:
                if latest_version.date >= today:
                    print('This version already exists.')
                    return
            version = api.collect()
            session.add(version)
        print('Version added to database.')
    except:
        logging.exception('message')


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbpath', help='sql connection here.')
    parser.add_argument('--setup', help='present to initialize database', action='store_true')
    return parser.parse_args()


def main(args=None):
    if args:
        args = parse_args(args)
        build_cmd(args.dbpath, args.setup)
    else:
        build()


if __name__ == '__main__':
    main(sys.argv[1:])
