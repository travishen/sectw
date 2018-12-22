![image](https://travis-ci.org/travishen/sectw.svg?branch=master)

Inspired by: [moskytw/zipcodetw](https://github.com/moskytw/zipcodetw)
----

Installation:
----

    pip install sectw

Source: [國土測繪圖資服務雲](https://maps.nlsc.gov.tw)
----
* [ListCounty](http://api.nlsc.gov.tw/other/ListCounty "http://api.nlsc.gov.tw/other/ListCounty")
* [ListTown](http://api.nlsc.gov.tw/other/ListTown/B "http://api.nlsc.gov.tw/other/ListTown/B")
* [ListLandSection](http://api.nlsc.gov.tw/other/ListLandSection/B/B01 "http://api.nlsc.gov.tw/other/ListLandSection/B/B01")

Usage
-----
Find land section code progressively and fuzzily:

    >>import sectw
    >>sectw.find('台北市松山區延吉段一小段18-1號')
    [('AD0609', 'A010609', 'AD060900180001', 'A01060900180001')]

Take top N result:

    >>import sectw
    >>sectw.find('延吉段', take=3)
    [('AD0609', 'A010609', '', ''), ('AD0611', 'A010611', '', ''), ('FA0201', 'F190201', '', '')]

Handling complex address:

    >>import sectw

    >>sectw.find_complex('臺南市六甲區港子頭段540,540-4地號')
    [('臺南市六甲區港子頭段540地號', [('DF4322', 'D174322', 'DF432205400000', 'D17432205400000')]),
     ('臺南市六甲區港子頭段540-4地號', [('DF4322', 'D174322', 'DF432205400004', 'D17432205400004')])]

    >>sectw.find_complex('雲林縣口湖鄉梧北段二五四之四十三、二五四之四十六地號；二崙鄉來惠段２５４地號；臺中市大甲區中山段254、256地號')
    [('雲林縣口湖鄉梧北段24-43地號', [('PE0783', 'P190783', 'PE078300240043', 'P19078300240043')]),
     ('雲林縣口湖鄉梧北段24-46地號', [('PE0783', 'P190783', 'PE078300240046', 'P19078300240046')]),
     ('二崙鄉來惠段254地號', [('PC0384', 'P110384', 'PC038402540000', 'P11038402540000')]),
     ('臺中市大甲區中山段254地號', [('BE3642', 'B113642', 'BE364202540000', 'B11364202540000')]),
     ('臺中市大甲區中山段256地號', [('BE3642', 'B113642', 'BE364202560000', 'B11364202560000')])]


Manually build a new dataset version:

    $ python -m sectw.builder


If you want to create database
-------------------------------

Setup database(e.g. postgresql):

    $ python -m sectw.builder --dbpath postgresql+psycopg2://username:password@host/dbname --setup

Build a new version:

    $ python -m sectw.builder --dbpath postgresql+psycopg2://username:password@host/dbname

Load from database

    >> import sectw
    >> sectw.load_db('postgresql+psycopg2://username:password@host/dbname', create_date='2017-11-16')
    >> sectw.find('台北市松山區延吉段一小段18-1號')

To-do
-------------------------------

* Test api
* Modify result format