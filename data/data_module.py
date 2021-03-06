# -*- coding:utf-8 -*-
from util.database import DB_CONN
from datetime import datetime
from pymongo import ASCENDING
from pandas import DataFrame

"""本地数据库获取数据"""
class DataModule:
    def __init__(self):
        pass

    def get_price(self, code=None, adj=None, begin_date=None, end_date=None):
        """
        get stock daily data
        :param code:
        :param adj: 默认不复权 ; hfq 后复权
        :param begin_date: 没有指定日期默认当前日期
        :param end_date:   没有指定结束日期,默认等于开始日期
        :return:
        """

        # 没有指定代码返回None
        if code is None:
            raise Exception('没有指定股票代码')

        # 没有指定开始日期,默认当前日期
        if begin_date is None:
            begin_date = datetime.now().strftime('%Y%m%d')

        # 没有指定结束日期,默认开始日期
        if end_date is None:
            end_date = begin_date

        collection = 'daily' if adj is None or adj == '' else 'daily_' + adj
        daily_cursor = DB_CONN[collection].find(
            {'code': code, 'date': {'$gte': begin_date, '$lte': end_date}},
            sort=[('date', ASCENDING)],
            projection={'_id': False}
        )

        # [{},{},{}]
        df_daily = DataFrame([daily for daily in daily_cursor])
        if len(df_daily.index) > 0:
            df_daily.set_index('date', inplace=True)
        else:
            print("数据为空!")
        # print(daily_cursor)  # <pymongo.cursor.Cursor object at 0x00000247A65D4C18>
        # for daily in daily_cursor:
        #       print(daily) #{'code': '000002.SZ', 'date': '20200506', 'amount': 2409411.108, ...}

        return df_daily

    def get_all_price_one_day(self, date, adj=None):
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        if not isinstance(date, str):
            date = date.strftime('%Y%m%d')

        collection = 'daily' if adj is None or adj == '' else 'daily_' + adj
        daily_cursor = DB_CONN[collection].find(
            {'date': date}, projection={'_id': False}
        )
        df_daily = DataFrame([daily for daily in daily_cursor])
        if len(df_daily.index) > 0:
            df_daily.set_index('code', inplace=True)
        else:
            print("数据为空!")

        return df_daily


if __name__ == '__main__':
    dm = DataModule()
    # df_daily = DataModule().get_price('000001.XSHG', begin_date='20200505', end_date='20200510')
    # print(df_daily)
    # df_daily = DataModule().get_price('000002.XSHE', adj='qfq', begin_date='20200505', end_date='20200510')
    # print(df_daily)
    df_daily = dm.get_all_price_one_day('20200803', adj='qfq')
    print(df_daily)
