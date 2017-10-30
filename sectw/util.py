#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Address function modificated from mosky's zipcodetw module
from __future__ import print_function
from __future__ import unicode_literals
import re
import json
import six
from .database.model import Version


class Address(object):
    TOKEN_RE = re.compile('''
        (?:
            (?P<no>\d+)
            |
            (?P<value>.+?)
        )
        (?:
            (?P<unit>[縣市鄉鎮市區段號]|地號|地段)
        )
    ''', re.X)

    NO = 0
    VALUE = 1
    UNIT = 2

    TO_REPLACE_RE = re.compile('''
        [ 　，台、；.之]
        |
        [０-９]
        |
        [一二三四五六七八九]?
        十?
        [一二三四五六七八九]
        (?=[號]|地號|地段)
    ''', re.X)

    DELIMITER = ','

    # the strs matched but not in here will be removed
    TO_REPLACE_MAP = {
        '.': DELIMITER, '，': DELIMITER, '、': DELIMITER, '；': DELIMITER,
        '之': '-', '台': '臺',
        '１': '1', '２': '2', '３': '3', '４': '4', '５': '5',
        '６': '6', '７': '7', '８': '8', '９': '9', '０': '0',
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9',
    }

    CHINESE_NUMERALS_SET = set('一二三四五六七八九十')

    @staticmethod
    def normalize(s):

        if isinstance(s, six.binary_type):
            s = s.decode('utf-8')

        def replace(m):

            found = m.group()

            if found in Address.TO_REPLACE_MAP:
                return Address.TO_REPLACE_MAP[found]

            # for '十一' to '九十九'
            if found[0] in Address.CHINESE_NUMERALS_SET:
                len_found = len(found)
                if len_found == 2:
                    return '1' + Address.TO_REPLACE_MAP[found[1]]
                if len_found == 3:
                    return Address.TO_REPLACE_MAP[found[0]] + Address.TO_REPLACE_MAP[found[2]]

            return ''

        s = Address.TO_REPLACE_RE.sub(replace, s)

        return s

    @staticmethod
    def tokenize(addr_str):
        return Address.TOKEN_RE.findall(Address.normalize(addr_str))

    def __init__(self, addr_str):
        self.tokens = Address.tokenize(addr_str)

    def __len__(self):
        return len(self.tokens)

    def flat(self, sarg=None, *sargs):
        return ''.join(''.join(token) for token in self.tokens[slice(sarg, *sargs)])

    def pick_to_flat(self, *idxs):
        return ''.join(''.join(self.tokens[idx]) for idx in idxs)

    def __repr__(self):
        return 'Address(%r)' % self.flat()


class LandCode(Address):
    COUNTY = 0
    TOWN = 1
    SECTOR = 2
    NUMBER = 4

    COUNTY_MATCH = ['縣', '市']
    TOWN_MATCH = ['鄉', '鎮', '區']
    SECTION_MATCH = ['段', '地段']
    NUMBER_MATCH = ['號', '地號']

    def __init__(self, land_str):
        Address.__init__(self, land_str)
        self.county, self.town, self.section, self.number = LandCode.get_value(self.tokens)

    @staticmethod
    def get_value(tokens):
        county = LandCode.get_first_value([token[Address.VALUE] + token[Address.UNIT]
                                           for token in tokens if token[Address.UNIT] in LandCode.COUNTY_MATCH])

        town = LandCode.get_first_value([token[Address.VALUE] + token[Address.UNIT]
                                         for token in tokens if token[Address.UNIT] in LandCode.TOWN_MATCH])

        section = LandCode.get_first_value([token[Address.VALUE] + token[Address.UNIT]
                                           for token in tokens if token[Address.UNIT] in LandCode.SECTION_MATCH])

        number = LandCode.get_first_value([token[Address.VALUE] + token[Address.UNIT]
                                           for token in tokens if token[Address.UNIT] in LandCode.NUMBER_MATCH])

        return county, town, section, number

    @staticmethod
    def get_first_value(lst):
        return next(iter(lst or []), None)


class Directory(object):

    def __init__(self, csv_path):
        self.version = Directory.load_csv(csv_path)

    @staticmethod
    def load_csv(csv_path):
        with open(csv_path, 'rb') as file:
            return json.load(file, object_hook=Version.from_dict)

    def find(self, addr_str):

        land_code = LandCode(addr_str)

        print(land_code.county, land_code.town, land_code.section, land_code.number)

        if land_code.county:
            counties = self.version.find(land_code.county)
        else:
            counties = self.version.counties

        towns = []
        if land_code.town:
            for county in counties:
                print(county)
                towns += county.find(land_code.town)
        else:
            for county in counties:
                towns += county.towns

        sections = []
        if land_code.section:
            for town in towns:
                sections += town.find(land_code.section)
        else:
            for town in towns:
                sections += town.lands

        print(len(counties), len(towns), len(sections))

        return sections








