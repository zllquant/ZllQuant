# -*- coding:utf-8 -*-
from util.database import DB_CONN
from abc import abstractmethod


class BaseFactor():
    def __init__(self, name):
        self.name = name
        self.collection = DB_CONN[name]

    @abstractmethod
    def compute(self, begin_date, end_date):
        pass
