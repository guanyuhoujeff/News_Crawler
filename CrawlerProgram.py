#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 23:28:44 2018

@author: jam
"""

from CrawlerPy import Crawler_for_chinatimes
from CrawlerPy import Crawler_for_cnyes
from CrawlerPy import Crawler_for_ltn
from CrawlerPy import Crawler_for_moneydj
from CrawlerPy import Crawler_for_udn
from CrawlerPy import Crawler_for_yahoo

import datetime

New_DataBase_path = "./NewsDB"

Crawler_for_chinatimes.Main(New_DataBase_path)
Crawler_for_cnyes.Main(New_DataBase_path)
Crawler_for_ltn.Main(New_DataBase_path)
Crawler_for_moneydj.Main(New_DataBase_path)
Crawler_for_udn.Main(New_DataBase_path)
Crawler_for_yahoo.Main(New_DataBase_path)

print("All Crawler Done At", datetime.datetime.now())