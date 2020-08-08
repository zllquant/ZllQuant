# -*- coding:utf-8 -*-
from util.database import DB_CONN
from abc import abstractmethod
import rqdatac as rqd
from pymongo import UpdateOne


class BaseFactor:
    def __init__(self, name):
        self.name = name
        self.collection = DB_CONN[name]

    def compute(self, begin_date, end_date):
        """
        计算区间因子并保存数据
        :param begin_date:
        :param end_date:
        :return:
        """
        dates = rqd.get_trading_dates(begin_date, end_date)
        dates = [i.strftime('%Y%m%d') for i in dates]
        for date in dates:
            # 调用子类的实现方法,计算因子
            factors = self.compute_one_day(date)
            update_requests = []
            for factor in factors:
                update_requests.append(
                    UpdateOne({'code': factor['code'], 'date': date},
                              {'$set': factor},
                              upsert=True)
                )
            if len(update_requests) > 0:
                update_result = self.collection.bulk_write(update_requests)
                print('保存-%s-%s数据 , 插入:%4d , 更新:%4d'
                      % (date, self.name, update_result.upserted_count, update_result.modified_count),
                      flush=True)

    @abstractmethod
    def compute_one_day(self, date):
        pass
