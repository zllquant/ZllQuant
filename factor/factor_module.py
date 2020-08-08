# -*- coding:utf-8 -*-
from util.database import DB_CONN
import pandas as pd
from datetime import datetime
from pymongo import ASCENDING


class FactorModule:
    def __init__(self):
        pass

    def get_stock_factor(self, code=None, factor=None, begin_date=None, end_date=None):
        """
        Get factor values of one stock between begin_date and end_date.
        :param code:
        :param factor:
        :param begin_date:
        :param end_date:
        :return:
        """

        # 没有指定代码返回None
        if code is None:
            raise Exception('没有指定股票代码')

        if factor is None or factor == '':
            raise Exception('没有指定因子名称')

        # 没有指定开始日期,默认当前日期
        if begin_date is None:
            begin_date = datetime.now().strftime('%Y%m%d')

        # 没有指定结束日期,默认开始日期
        if end_date is None:
            end_date = begin_date

        factor_cursor = DB_CONN[factor].find(
            {'code': code, 'name': factor, 'date': {'$gte': begin_date, '$lte': end_date}}
            , sort=[('date', ASCENDING)]
            , projection={'_id': False}
        )

        # 多个字典一秒变DataFrame!
        df_factor = pd.DataFrame([doc for doc in factor_cursor])
        # 这个df可能为空
        if df_factor.index.size > 0:
            df_factor.set_index('date', inplace=True)

        return df_factor

    def get_factor_one_day(self, factor=None, date=None):
        """
        get a factor value of all codes in one day
        获取所有股票在某个交易日的某个因子值
        :param factor:
        :param date:
        :return:
        """

        if factor is None or factor == '':
            raise Exception('没有指定因子名称')

        if date is None:
            date = datetime.now().strftime('%Y%m%d')

        factor_cursor = DB_CONN[factor].find(
            {'name': factor, 'date': date}
            , projection={'_id': False}
        )
        # 多个字典一秒变DataFrame!
        df_factor = pd.DataFrame([doc for doc in factor_cursor])
        # 这个df可能为空
        if df_factor.index.size > 0:
            df_factor.set_index('code', inplace=True)
        else:
            print("数据为空!")

        return df_factor


if __name__ == '__main__':
    fm = FactorModule()
    fm.get_factor_one_day('pe')
