# -*- coding:utf-8 -*-
from factor.base_factor import BaseFactor
from data.data_module import DataModule
import rqdatac as rqd

rqd.init()
"""
PE因子
"""


class PEFactor(BaseFactor):
    def __init__(self):
        BaseFactor.__init__(self, 'pe_ratio_ttm')

    def compute_one_day(self, date):
        # 用不到,只是为了练习,实际取米筐数据存
        # dm = DataModule()
        # 某天所有股票数据
        # df_daily = dm.get_all_price_one_day(date)
        stocklist = rqd.all_instruments('CS', date)['order_book_id'].tolist()
        pe = rqd.get_factor(stocklist, self.name, date, date)
        factors = []
        for code in pe.index:
            factors.append(
                {'date': date, 'code': code, self.name: round(pe[code], 2)}
            )

        return factors


if __name__ == '__main__':
    PEFactor().compute(begin_date='20200101', end_date='20200805')
