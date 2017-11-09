#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Address function modified from mosky's zipcodetw module
from __future__ import print_function
from __future__ import unicode_literals
import re
import json
import six
import logging
from .database.model import hook, Version
from .database import config


class Address(object):
    TOKEN_RE = re.compile('''
        (?:
            (?P<value>..+?)
        )
        (?:
            (?P<unit>區段|[縣市鄉鎮市區村里段號]|地號|地段)
        )
    ''', re.X)

    S_TOKEN_RE = re.compile('''
        (?:
            (?P<value>.+?)
        )
        (?:
            (?P<unit>小段|地號|號)
        )
    ''', re.X)

    VALUE = 0
    UNIT = 1

    GLOBAL_REPLACE_RE = re.compile('''
        [ 　,.，、；台]
        |
        [０-９]    
    ''', re.X)

    NO_HYPHEN_REPLACE_RE = re.compile('''
        [之–—]
    ''', re.X)

    NO_NUM_REPLACE_RE = re.compile('''
        (?:
            [一二三四五六七八九]?
            [一二三四五六七八九]?
            十?
            [一二三四五六七八九]
            |
            [十]
        )
        (?=-|號|地號)
    ''', re.X)

    # the strs matched but not in here will be removed
    TO_REPLACE_MAP = {
        '之': '-', '–': '-', '—': '-',
        '台': '臺',
        '１': '1', '２': '2', '３': '3', '４': '4', '５': '5',
        '６': '6', '７': '7', '８': '8', '９': '9', '０': '0',
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9', '十': '10',
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

            return ''

        def replace_num(m):

            found = m.group()

            if found in Address.TO_REPLACE_MAP:
                return Address.TO_REPLACE_MAP[found]

            if found[0] in Address.CHINESE_NUMERALS_SET:
                # for '十一' to '九十九'
                if u'十' in found[0]:
                    len_found = len(found)
                    if len_found == 2:
                        return '1' + Address.TO_REPLACE_MAP[found[1]]
                    if len_found == 3:
                        return Address.TO_REPLACE_MAP[found[0]] + Address.TO_REPLACE_MAP[found[2]]
                else:
                    return ''.join(Address.TO_REPLACE_MAP[t] for t in found)

            return ''

        s = Address.GLOBAL_REPLACE_RE.sub(replace, s)

        s = Address.NO_HYPHEN_REPLACE_RE.sub(replace, s)

        while True:
            replaced = Address.NO_NUM_REPLACE_RE.sub(replace_num, s)
            if s == replaced:
                break
            s = replaced

        return s

    @staticmethod
    def tokenize(addr_str):

        addr_str = Address.normalize(addr_str)
        addr_list = Address.split(addr_str)
        tokens = []

        if len(addr_list) > 0:
            # make exception if 段 unit only has one character
            if len(addr_list[0]) == 2:
                token = (addr_list[0][0], '段')
                tokens.append(token)
            tokens += Address.TOKEN_RE.findall(Address.normalize(addr_list[0]))

        if len(addr_list) > 1:
            tokens += Address.S_TOKEN_RE.findall(Address.normalize(addr_list[1]))
        return tokens

    @staticmethod
    def split(addr_str):

        # split 松山區西松段一小段 to ['松山區西松段', '一小段'] and fit to different pattern
        addr_list = list(filter(None, re.split('(段)', addr_str, 1)))
        addr_list[:2] = [''.join(addr_list[:2])]
        return addr_list

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
    SECTION_MATCH = ['段', '地段', '區段']
    SMALL_SECTION_MATCH = ['小段']
    NUMBER_MATCH = ['號', '地號']

    def __init__(self, addr_str):
        super(LandCode, self).__init__(addr_str)
        self.county, self.town, self.section, self.small_section, self.number = LandCode.get_value(self.tokens)

    @staticmethod
    def get_value(tokens):
        county = LandCode.get_first_match([token[Address.VALUE] + token[Address.UNIT]
                                           for token in tokens if token[Address.UNIT]
                                           in LandCode.COUNTY_MATCH])

        town = LandCode.get_first_match([token[Address.VALUE] + token[Address.UNIT]
                                         for token in tokens if token[Address.UNIT]
                                         in LandCode.TOWN_MATCH])

        section = LandCode.get_first_match([token[Address.VALUE] + token[Address.UNIT]
                                            for token in tokens if token[Address.UNIT]
                                            in LandCode.SECTION_MATCH])

        small_section = LandCode.get_first_match([token[Address.VALUE] + token[Address.UNIT]
                                                  for token in tokens if token[Address.UNIT]
                                                  in LandCode.SMALL_SECTION_MATCH])

        number = LandCode.get_first_match([token[Address.VALUE]
                                           for token in tokens if token[Address.UNIT]
                                           in LandCode.NUMBER_MATCH])

        return county, town, section, small_section, number

    @staticmethod
    def get_first_match(lst):
        return next(iter(lst or []), '')


class Directory(object):

    def __init__(self, csv_path):
        self.version = Directory.load_csv(csv_path)

    @staticmethod
    def load_csv(csv_path):
        with open(csv_path, 'rb') as file:
            return json.load(file, object_hook=hook)

    def load_db(self, db_path, create_date=None):
        try:
            config.setup_session(db_path)
            with config.session_scope() as session:
                if not create_date:
                    latest_version = Version.get_latest_version(session)
                    create_date = latest_version.date
                self.version = Version.get_version(session, create_date)
        except:
            logging.exception('message')

    def find(self, addr_str, take=1):

        # state the costs of each type of error for fuzzy_counts sorting
        FUZZY_MATCH_COSTS = (3, 1, 1)

        land_code = LandCode(addr_str)

        if land_code.county:
            counties = self.version.find(land_code.county)
        else:
            counties = self.version.counties

        towns = []
        if land_code.town:
            for county in counties:
                towns += county.find(land_code.town)
        else:
            for county in counties:
                towns += county.towns

        sections = []
        if land_code.section:
            for town in towns:
                for section in town.sections:
                    section.count_section_fuzzy(land_code.section)
                    if land_code.small_section:
                        section.count_small_section_fuzzy(land_code.small_section)
                    sections.append(section)
            sections.sort(key=lambda x: sum(map(lambda x_y: x_y[0]*x_y[1], zip(x.section_fc, FUZZY_MATCH_COSTS))))
            if land_code.small_section:
                sections.sort(key=lambda x: sum(map(lambda x_y: x_y[0]*x_y[1], zip(x.small_section_fc, FUZZY_MATCH_COSTS))))
        elif land_code.small_section:
            for town in towns:
                for section in town.sections:
                    section.count_small_section_fuzzy(land_code.small_section)
                    sections.append(section)
            sections.sort(key=lambda x: sum(map(lambda x_y: x_y[0]*x_y[1], zip(x.small_section_fc, FUZZY_MATCH_COSTS))))

        number = ''
        if land_code.number:
            numbers = land_code.number.split('-')
            if len(numbers) == 1:
                numbers.append('')
            number = numbers[0].zfill(4) + numbers[1].zfill(4)

        return json.dumps([section.__repr__(number) for section in sections[:take]])





























