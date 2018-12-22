#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import sectw
from sectw.util import LandAddress


def test_land_address_init():

    expected_tokens = [('台北', '市'), ('松山', '區'), ('延吉', '段'), ('一', '小段'), ('18-1', '號')]
    assert LandAddress('台北市松山區延吉段一小段18-1號').tokens == expected_tokens
    assert LandAddress('台北市松山區延吉段一小段18-1號').tokens == expected_tokens

    obj = LandAddress('台北市松山區延吉段一小段18-1號')
    assert obj.county == ('台北', '市')
    assert obj.town == ('松山', '區')
    assert obj.village == ('', '')
    assert obj.section == ('延吉', '段')
    assert obj.small_section == ('一', '小段')
    assert obj.number == ('18-1', '號')


def test_land_address_pick_to_flat():
    obj = LandAddress('台北市松山區延吉段一小段18-1號')
    assert obj.pick_to_flat(0, 1, 2, 3, 4, 5) == '台北市松山區延吉段一小段18-1號'
    assert obj.pick_to_flat(0, 5) == '台北市18-1號'


def test_land_address_get_digit():
    obj = LandAddress('台北市松山區延吉段一小段18-1號')
    assert obj.get_digit('市') == 0
    assert obj.get_digit('區') == 1
    assert obj.get_digit('村') == 2
    assert obj.get_digit('段') == 3
    assert obj.get_digit('小段') == 4
    assert obj.get_digit('號') == 5


def test_find():
    expected_result = [('AD0609', 'A010609', 'AD060900180001', 'A01060900180001')]
    assert sectw.find('台北市松山區延吉段一小段18-1號') == expected_result

    expected_result = [('AD0609', 'A010609', '', ''), ('AD0611', 'A010611', '', ''), ('FA0201', 'F190201', '', '')]
    assert sectw.find('延吉段', take=3) == expected_result

    expected_result = [('臺南市六甲區港子頭段540地號', [('DF4322', 'D174322', 'DF432205400000', 'D17432205400000')]),
                       ('臺南市六甲區港子頭段540-4地號', [('DF4322', 'D174322', 'DF432205400004', 'D17432205400004')])]
    assert sectw.find_complex('臺南市六甲區港子頭段540,540-4地號', take=1) == expected_result

    expected_result = [('雲林縣口湖鄉梧北段24-43地號', [('PE0783', 'P190783', 'PE078300240043', 'P19078300240043')]),
                       ('雲林縣口湖鄉梧北段24-46地號', [('PE0783', 'P190783', 'PE078300240046', 'P19078300240046')]),
                       ('二崙鄉來惠段254地號', [('PC0384', 'P110384', 'PC038402540000', 'P11038402540000')]),
                       ('臺中市大甲區中山段254地號', [('BE3642', 'B113642', 'BE364202540000', 'B11364202540000')]),
                       ('臺中市大甲區中山段256地號', [('BE3642', 'B113642', 'BE364202560000', 'B11364202560000')])]

    assert sectw.find_complex('雲林縣口湖鄉梧北段二五四之四十三、二五四之四十六地號；二崙鄉來惠段２５４地號；臺中市大甲區中山段254、256地號') == expected_result
