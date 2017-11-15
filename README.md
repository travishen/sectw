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
    [{"SN6": "AD0609", "SN7": "A010609", "SLN14": "AD060900180001", "SLN15": "A01060900180001"}]

Take top N result:

    >>import sectw
    >>sectw.find('延吉段', take=3)
    [{"SN6": "AD0609", "SN7": "A010609", "SLN14": null, "SLN15": null},{"SN6": "AD0611", "SN7": "A010611", "SLN14": null, "SLN15": null}, {"SN6": "FA0201", "SN7": "F190201", "SLN14": null, "SLN15": null}]

Handling complex address:

    >>import sectw

    >>sectw.find_complex('臺南市六甲區港子頭段540,540-4地號', take=1)
    [{'R': '[{"SLN15": "R09032205400000", "SN6": "RC0322", "SN7": "R090322", "SLN14": "RC032205400000"}]', 'A': '臺南市六甲區港子頭段540地號'}, {'R': '[{"SLN15": "R09032205400004", "SN6": "RC0322", "SN7": "R090322", "SLN14":
     "RC032205400004"}]', 'A': '臺南市六甲區港子頭段540-4地號'}]


    >>sectw.find_complex('雲林縣口湖鄉梧北段二五四之四十三、二五四之四十六地號；二崙鄉來惠段２５４地號；臺中市大甲區中山段254、256地號')
    [{'R': '[{"SLN15": "P19078300240043", "SN6": "PE0783", "SN7": "P190783", "SLN14": "PE078300240043"}]', 'A': '雲林縣口湖鄉梧北段24-43地號'}, {'R': '[{"SLN15": "P19078300240046", "SN6": "PE0783", "SN7": "P190783", "SLN14":
     "PE078300240046"}]', 'A': '雲林縣口湖鄉梧北段24-46地號'}, {'R': '[{"SLN15": "P11038402540000", "SN6": "PC0384", "SN7": "P110384", "SLN14": "PC038402540000"}]', 'A': '二崙鄉來惠段254地號'}, {'R': '[{"SLN15": "B1136420254
    0000", "SN6": "BE3642", "SN7": "B113642", "SLN14": "BE364202540000"}]', 'A': '臺中市大甲區中山段254地號'}, {'R': '[{"SLN15": "B11364202560000", "SN6": "BE3642", "SN7": "B113642", "SLN14": "BE364202560000"}]', 'A': '臺中
    市大甲區中山段256地號'}]


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