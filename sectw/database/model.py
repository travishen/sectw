#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import Integer, Column, ForeignKey, Sequence, String, Date, Unicode
from sqlalchemy.orm import relationship, subqueryload
from json import JSONEncoder
import regex
from . import Base


class ORMEncoder(JSONEncoder):
    def default(self, obj):
        # convert object to a dict
        d = {}
        if isinstance(obj, Version):
            return {'date': str(obj.date), 'counties': list(obj.counties)}
        if isinstance(obj, County):
            return {'code': obj.code, 'name': obj.name, 'towns': obj.towns}
        if isinstance(obj, Town):
            return {'code': obj.code, 'name': obj.name, 'sections': obj.sections}
        if isinstance(obj, Section):
            return {'code': obj.code, 'name': obj.name, 'office': obj.office}

        d.update(obj.__dict__)
        return d


def hook(dict):
    if dict.get('counties'):
        version = Version()
        version.__dict__.update(dict)
        return version
    if dict.get('towns'):
        county = County()
        county.__dict__.update(dict)
        return county
    if dict.get('sections'):
        town = Town()
        town.__dict__.update(dict)
        return town
    else:
        section = Section()
        section.__dict__.update(dict)
        return section


class Version(Base):
    __tablename__ = 'version'
    id = Column(Integer, Sequence('version_id_seq'), primary_key=True, nullable=False)
    date = Column(Date)
    counties = relationship('County')

    @staticmethod
    def get_latest_version(session):
        return session.query(Version).order_by(Version.date.desc()).first()

    @staticmethod
    def get_version(session, date):
        data = session.query(Version) \
            .filter(Version.date == date) \
            .option(subqueryload(Version.counties)
                    .subqueryload(County.towns)
                    .subqueryload(Town.sections))
        return data


class County(Base):
    __tablename__ = 'county'
    id = Column(Integer, Sequence('county_id_seq'), primary_key=True, nullable=False)
    code = Column(String(1))
    name = Column(Unicode(5))
    version_id = Column(Integer, ForeignKey('version.id'))
    version = relationship('Version', back_populates='counties')
    towns = relationship('Town')


class Town(Base):
    __tablename__ = 'town'
    id = Column(Integer, Sequence('county_id_seq'), primary_key=True, nullable=False)
    code = Column(String(3))
    name = Column(Unicode(5))
    county_id = Column(Integer, ForeignKey('county.id'))
    county = relationship('County', back_populates='towns')
    sections = relationship('Section')


class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, Sequence('section_id_seq'), primary_key=True, nullable=False)
    code = Column(String(4))
    office = Column(String(2))
    name = Column(Unicode(20))
    code6 = Column(String(6))
    code7 = Column(String(7))
    town_id = Column(Integer, ForeignKey('town.id'))
    town = relationship('Town', back_populates='sections')





