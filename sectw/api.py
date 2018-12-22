#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
import requests
import datetime
from xml.etree import ElementTree
from .util import Address
from .database.model import Version, County, Town, Section


def collect():
    print('collecting...')
    date = datetime.date.today()
    counties = list_county()
    version = Version(date=date, counties=counties)
    return version


def list_county():
    counties = []
    try:
        url = 'http://api.nlsc.gov.tw/other/ListCounty'
        res = requests.get(url)
        tree = ElementTree.fromstring(res.content)
        for child in tree.iterfind('countyItem'):
            code = child.findtext('countycode')
            name = child.findtext('countyname')
            towns = list_town(code)
            county = County(code=code, name=name, towns=towns)
            counties.append(county)
    except Exception as e:
        logging.error('please verify this url:{}'.format(url))
        logging.exception(e)
    return counties


def list_town(county_code):
    towns = []
    try:
        url = 'http://api.nlsc.gov.tw/other/ListTown/{}'.format(county_code)
        res = requests.get(url=url)
        tree = ElementTree.fromstring(res.content)
        for child in tree.iterfind('townItem'):
            code = child.findtext('towncode')
            name = child.findtext('townname')
            sections = list_section(county_code, code)
            town = Town(code=code, name=name, sections=sections)
            towns.append(town)
    except Exception as e:
        logging.error('please verify this url:{}'.format(url))
        logging.exception(e)
    return towns


def list_section(county_code, town_code):
    sections = []
    try:
        url = 'http://api.nlsc.gov.tw/other/ListLandSection/{}/{}'.format(county_code, town_code)
        res = requests.get(url=url)
        tree = ElementTree.fromstring(res.content)
        for child in tree.iterfind('sectItem'):
            code = child.findtext('sectcode')
            name = child.findtext('sectstr')
            address = Address(name)
            office = child.findtext('office')
            code6 = office + code
            code7 = town_code + code
            section = Section(code=code,
                              section_name=address.pick_to_flat(0) if len(address.tokens) > 0 else name,
                              small_section_name=address.pick_to_flat(1) if len(address.tokens) > 1 else '',
                              office=office,
                              code6=code6,
                              code7=code7)
            sections.append(section)
    except Exception as e:
        logging.error('please verify this url:{}'.format(url))
        logging.exception(e)
    return sections
