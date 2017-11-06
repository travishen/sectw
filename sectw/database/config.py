#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import create_engine
from contextlib import contextmanager
from . import Base, Session

engine = None


def setup_session(dbpath):
    global engine
    engine = create_engine(dbpath)
    Session.configure(bind=engine)


def init():
    print('initialize database...')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

