API
----
Source: [國土測繪圖資服務雲](https://maps.nlsc.gov.tw "https://maps.nlsc.gov.tw")
* [ListCounty](http://api.nlsc.gov.tw/other/ListCounty "http://api.nlsc.gov.tw/other/ListCounty")
* [ListTown](http://api.nlsc.gov.tw/other/ListTown/B "http://api.nlsc.gov.tw/other/ListTown/B")
* [ListLandSection](http://api.nlsc.gov.tw/other/ListLandSection/B/B01 "http://api.nlsc.gov.tw/other/ListLandSection/B/B01")

Usage
-----
If you want to create database

* Setup database(e.g. postgresql):

    $ python build.py --dburl postgresql+psycopg2://username:password@host/dbname --setup

* Build a new version:

    $ python build.py --dburl postgresql+psycopg2://username:password@host/dbname