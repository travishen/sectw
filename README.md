Source: [國土測繪圖資服務雲](https://maps.nlsc.gov.tw "https://maps.nlsc.gov.tw")
----
* [ListCounty](http://api.nlsc.gov.tw/other/ListCounty "http://api.nlsc.gov.tw/other/ListCounty")
* [ListTown](http://api.nlsc.gov.tw/other/ListTown/B "http://api.nlsc.gov.tw/other/ListTown/B")
* [ListLandSection](http://api.nlsc.gov.tw/other/ListLandSection/B/B01 "http://api.nlsc.gov.tw/other/ListLandSection/B/B01")

Usage
-----
Find land section code progressively and fuzzily:

    >>import sectw
    >>sectw.find('台北市松山區延吉段一小段18-1號')
    u'[{"S": "延吉段一小段", "SN6": "AD0609", "SN7": "A010609", "SLN14": "AD060900180001", "SLN15": "A01060900180001"}]'

Take top N result:

    >>import sectw
    >>sectw.find('延吉段', take=3)
    u'[{"S": "延吉段一小段", "SN6": "AD0609", "SN7": "A010609", "SLN14": null, "SLN15": null},{"S": "延吉段二小段", "SN6": "AD0611", "SN7": "A010611", "SLN14": null, "SLN15": null}, {"S": "延吉段", "SN6": "FA0201", "SN7": "F190201", "SLN14": null, "SLN15": null}]'

Handling complex address:

    >>import sectw

    >>sectw.find_complex('臺南市六甲區港子頭段540,540-4地號', take=1)
    u'['[{"S": "港子頭段", "SN6": "RC0322", "SN7": "R090322", "SLN14": "RC032205400000", "SLN15": "R09032205400000"}]', '[{"S": "港子頭段", "SN6": "RC0322", "SN7": "R090322", "SLN14": "R
    C032205400004", "SLN15": "R09032205400004"}]']'

    >>sectw.find_complex('雲林縣口湖鄉椬梧段二五四之四十三、二五四之四十六地號；二崙鄉來惠段２５４地號；臺中市大甲區中山段254、256地號')
    u'['[{"S": "椬梧段", "SN6": "PE0653", "SN7": "P190653", "SLN14": "PE065302540043", "SLN15": "P19065302540043"}]', '[{"S": "椬梧段", "SN6": "PE0653", "SN7": "P190653", "SLN14": "PE065302540046", "SLN15": "
    P19065302540046"}]', '[{"S": "來惠段", "SN6": "PC0384", "SN7": "P110384", "SLN14": "PC038402540000", "SLN15": "P11038402540000"}]', '[{"S": "中山段", "SN6": "BE3642", "SN7": "B113642", "SLN1
    4": "BE364202540000", "SLN15": "B11364202540000"}]', '[{"S": "中山段", "SN6": "BE3642", "SN7": "B113642", "SLN14": "BE364202560000", "SLN15": "B11364202560000"}]']'

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