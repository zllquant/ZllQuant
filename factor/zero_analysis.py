import rqdatac as rqd
from util.selectstock import *

rqd.init()


class ZeroPortfolioAnalysis:
    def __init__(self, factor, begin_date=None, end_date=None, interval=5, group=10):
        self.factor = factor
        self.begin_date = begin_date
        self.end_date = end_date
        self.interval = interval
        self.group = group

    def select_stock(self, date):
        universe = get_universe(date)
        universe = drop_suspended(universe, date)
        universe = drop_st(universe, date)
        universe = drop_recently_listed(universe, date)

        return universe

    def analyze(self):
        dates = rqd.get_trading_dates(self.begin_date, self.end_date)

        for index in range(0, len(dates), self.interval):
            date = dates[index]
            universe = self.select_stock(date)

            factor_df = rqd.get_factor(universe, self.factor, date, date)[lambda x: x > 0]
            # 所有股票数量
            size = len(factor_df)
            # 每档数量
            position_size = int(size / self.group)
            top_group = factor_df.nsmallest(position_size).index.tolist()
            bottom_group = factor_df.nlargest(position_size).index.tolist()


if __name__ == '__main__':
    ZeroPortfolioAnalysis(
        'pe_ratio_ttm',
        begin_date='20150101',
        end_date='20200806',
        interval=20,
        group=10
    ).analyze()
