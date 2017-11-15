#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
            (?P<value>.+?)
        )
        (?:
            (?P<unit>地號|地段|小段|區段|鎮段|鎮區|市區|[縣市鄉鎮市區村里段號])
        )
    ''', re.X)

    VALUE = 0
    UNIT = 1
    
    GLOBAL_REPLACE_RE = re.compile('''
        [ 　台]
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
        )
        (?=-|號|地號|$)
    ''', re.X)

    # the strs matched but not in here will be removed
    TO_REPLACE_MAP = {
        '之': '-', '–': '-', '—': '-',
        '台': '臺',
        '１': '1', '２': '2', '３': '3', '４': '4', '５': '5',
        '６': '6', '７': '7', '８': '8', '９': '9', '０': '0',
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9',
    }

    CHINESE_NUMERALS_SET = set('一二三四五六七八九')

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
                len_found = len(found)
                if len_found == 2:
                    return '1' + Address.TO_REPLACE_MAP[found[1]]
                if len_found == 3:
                    return Address.TO_REPLACE_MAP[found[0]] + Address.TO_REPLACE_MAP[found[2]]

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
    def tokenize(addr_str, normalize=True):
        if normalize:
            addr_str = Address.normalize(addr_str)
        return Address.TOKEN_RE.findall(addr_str)    

    def __init__(self, addr_str, normalize=True):
        self.tokens = Address.tokenize(addr_str, normalize)

    def __len__(self):
        return len(self.tokens)

    @staticmethod
    def flat(tokens, sarg=None, *sargs):
        return ''.join(''.join(token) for token in tokens[slice(sarg, *sargs)])

    def pick_to_flat(self, *idxs):
        return ''.join(''.join(self.tokens[idx]) for idx in idxs)

    def __repr__(self):
        return 'Address(%r)' % Address.flat(self.tokens)


class LandCode(Address):

    COUNTY_DIGIT = 0
    TOWN_DIGIT = 1
    VILLAGE_DIGIT = 2
    SECTION_DIGIT = 3
    SMALL_SECTION_DIGIT = 4
    NUMBER_DIGIT = 5

    COUNTY_MATCH = ['縣', '市']
    TOWN_MATCH = ['鄉', '鎮', '區', '市區', '鎮區']
    VILLAGE_MATCH = ['村', '里']
    SECTION_MATCH = ['段', '地段', '區段', '鎮段']
    SMALL_SECTION_MATCH = ['小段']
    NUMBER_MATCH = ['號', '地號']

    TOKEN_RE = re.compile('''
        (?:
            (?P<value>..+?)
        )
        (?:
            (?P<unit>[縣市鄉鎮市區村里])
        )
    ''', re.X)

    S_TOKEN_RE = re.compile('''
        (?:
            (?P<value>.+?)
        )
        (?:
            (?P<unit>地段|段|小段|地號|號)
        )
    ''', re.X)

    SEP_SIGN = ','

    @staticmethod
    def get_value(tokens, units):

        def get_first_match(lst):
            return next(iter(lst or []), ('', ''))

        def get_all_matches(ts, us):
            return [(t[Address.VALUE], t[Address.UNIT]) for t in ts if t[Address.UNIT] in us]

        all_matches = get_all_matches(tokens, units)

        return get_first_match(all_matches)

    def __init__(self, addr_str, normalize=False, single=False):
        super(LandCode, self).__init__(addr_str, normalize)
        self.county = LandCode.get_value(self.tokens, LandCode.COUNTY_MATCH)
        self.town = LandCode.get_value(self.tokens, LandCode.TOWN_MATCH)
        self.village = LandCode.get_value(self.tokens, LandCode.VILLAGE_MATCH)
        self.section = LandCode.get_value(self.tokens, LandCode.SECTION_MATCH)
        self.small_section = LandCode.get_value(self.tokens, LandCode.SMALL_SECTION_MATCH)
        self.number = LandCode.get_value(self.tokens, LandCode.NUMBER_MATCH)

    @staticmethod
    def singularize_address(tokens):
        
        def flag(ts):
            flags = []
            for i, t in enumerate(ts):
                try:
                    cut_here = LandCode.get_digit(t[1]) - LandCode.get_digit(ts[i + 1][1]) > 0
                    flags.append(cut_here)
                except IndexError:
                    flags.append(True)

            return [ts[i] + (f, ) for i, f in enumerate(flags)]
        
        def pre_flat(ts):
            results = []
            fr = 0
            for i, t in enumerate(ts):
                to = i + 1
                if t[2]:
                    results.append((fr, to))
                    fr = to
            return results

        flagged_tokens = flag(tokens)
        to_flat = pre_flat(flagged_tokens)

        return [Address.flat(tokens, fr, to) for fr, to in to_flat]

    @staticmethod
    def flat_token(token):
        return token[0] + token[1]

    @staticmethod
    def singularize_number(addr_str):

        f = LandCode.flat_token

        ins = LandCode(addr_str, normalize=False, single=False)

        if ins.number:
            value = re.sub(r'[.、；，+及和|以及]', ',', ins.number[0])
            ns = [n for n in re.split(LandCode.SEP_SIGN, value) if n]

            # clear other unit's value
            front_str = f(ins.county) + f(ins.town) + f(ins.village) + f(ins.section) + f(ins.small_section)
            front_str = ''.join(e for e in front_str if e.isalnum())
            return [front_str + n + ins.number[1] for n in ns]

        return []
                        
    @classmethod        
    def get_digit(cls, unit):
        if unit in cls.COUNTY_MATCH:
            return cls.COUNTY_DIGIT
        if unit in cls.TOWN_MATCH:
            return cls.TOWN_DIGIT
        if unit in cls.VILLAGE_MATCH:
            return cls.VILLAGE_DIGIT
        if unit in cls.SECTION_MATCH:
            return cls.SECTION_DIGIT
        if unit in cls.NUMBER_MATCH:
            return cls.NUMBER_DIGIT
        return False


class Directory(object):

    def __init__(self, csv_path):
        self.version = Directory.load_csv(csv_path)

    @staticmethod
    def load_csv(csv_path):
        with open(csv_path, 'r') as file:
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
        costs = (3, 1, 1)

        def sum_cost(fuzzy_counts):
            return sum(map(lambda x_y: x_y[0]*x_y[1], zip(fuzzy_counts, costs)))

        land_code = LandCode(addr_str, normalize=True, single=True)

        f = LandCode.flat_token

        county = f(land_code.county)
        town = f(land_code.town)
        section = f(land_code.section)
        small_section = f(land_code.small_section)
        number = land_code.number

        if county:
            counties = self.version.find(county)
        else:
            counties = self.version.counties

        towns = []
        if town:
            for c in counties:
                towns += c.find(town)
        else:
            for c in counties:
                towns += c.towns

        sections = []
        if section:
            for t in towns:
                for s in t.sections:
                    s.count_section_fuzzy(section)
                    if small_section:
                        s.count_small_section_fuzzy(small_section)
                    sections.append(s)

            sections.sort(key=lambda x: sum_cost(x.section_fc))

            if small_section:
                sections.sort(key=lambda x: sum_cost(x.small_section_fc))

        elif small_section:
            for t in towns:
                for s in t.sections:
                    s.count_small_section_fuzzy(small_section)
                    sections.append(s)

            sections.sort(key=lambda x: sum_cost(x.small_section_fc))

        digit = ''
        if number[0]:
            digits = number[0].split('-')
            if len(digits) == 1:
                digits.append('')
            digit = digits[0].zfill(4) + digits[1].zfill(4)

        return json.dumps([s.get_val(digit) for s in sections[:take]])

    def find_complex(self, addr_str, take=1):

        # separate addresses
        tokens = Address.tokenize(addr_str, normalize=False)

        addrs = LandCode.singularize_address(tokens)

        parsed_addrs = []

        for addr in addrs:
            parsed_addrs += LandCode.singularize_number(addr)

        return [{'A': Address.normalize(addr), 'R': self.find(addr, take=take)} for addr in parsed_addrs]



























