API
----
Source: [國土測繪圖資服務雲](https://maps.nlsc.gov.tw "https://maps.nlsc.gov.tw")
* [ListCounty](http://api.nlsc.gov.tw/other/ListCounty "http://api.nlsc.gov.tw/other/ListCounty")
* [ListTown](http://api.nlsc.gov.tw/other/ListTown/B "http://api.nlsc.gov.tw/other/ListTown/B")
* [ListLandSection](http://api.nlsc.gov.tw/other/ListLandSection/B/B01 "http://api.nlsc.gov.tw/other/ListLandSection/B/B01")

Usage
-----
Find land section code fuzzily:

..code-block:: python

    >>import sectw
    >>sectw.find('台北市松山區延吉段一小段18-1號')
    u'[{"S": "延吉段一小段", "SN6": "AD0609", "SN7": "A010609", "SLN14": "AD060900180001", "SLN15": "A01060900180001"}]'

Take top 3 result:

..code-block:: python

    >>import sectw
    >>sectw.find('延吉段', take=3)
    u'[{"S": "延吉段一小段", "SN6": "AD0609", "SN7": "A010609", "SLN14": null, "SLN15": null},
    {"S": "延吉段二小段", "SN6": "AD0611", "SN7": "A010611", "SLN14": null, "SLN15": null},
    {"S": "延吉段", "SN6": "FA0201", "SN7": "F190201", "SLN14": null, "SLN15": null}]'

Manually build a new version:

.. code-block:: bash

    $ python -m sextw.builder

If you want to create database

* Setup database(e.g. postgresql):

.. code-block:: bash

    $ python -m sextw.builder --dburl postgresql+psycopg2://username:password@host/dbname --setup

* Build another version:

.. code-block:: bash

    $ python -m sextw.builder --dburl postgresql+psycopg2://username:password@host/dbname

* Load from database

.. code-block:: python

    >> import sectw
    >> sectw.load_db('postgresql+psycopg2://username:password@host/dbname')
    >> sectw.find('台北市松山區延吉段一小段18-1號')