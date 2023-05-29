#!/usr/bin/python
# -*- coding: utf-8 -*-
from model.conn import *

query = "select * from BA1010 where rownum < 10"

execQuery(query)