# -*- coding:utf-8 -*-
from pymongo import MongoClient
from util.password import *

DB_CONN = MongoClient(host=IP, port=27017)[Database]
DB_CONN.authenticate(user, password)
