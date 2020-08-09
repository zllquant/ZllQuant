import rqdatac as rqd
from util.selectstock import *
import logging
import pandas as pd
import matplotlib.pyplot as plt

rqd.init()


class ZeroPortfolioAnalysis:
    def __init__(self, factor, begin_date=None, end_date=None, interval=5, group=10, benchmark='000300.XSHG'):
        self.factor = factor
        self.begin_date = begin_date
        self.end_date = end_date
        self.interval = interval
        self.group = group
        self.benchmark = benchmark

    @staticmethod
    def __select_stock(date):
        universe = get_universe(date)
        universe = drop_suspended(universe, date)
        universe = drop_st(universe, date)
        universe = drop_recently_listed(universe, date)

        return universe

    def analyze(self):
        dates = rqd.get_trading_dates(self.begin_date, self.end_date)
        top_group, bottom_group = [], []
        last_date = None
        df_profit = pd.DataFrame(columns=['top', 'bottom', 'benchmark'])
        # 间隔一段时间遍历交易日
        for index in range(0, len(dates), self.interval):
            date = dates[index]
            print("当前日期:", date)
            if last_date is None:
                df_profit.loc[date] = {'top': 0, 'bottom': 0, 'benchmark': 0}
            else:
                # 股票收盘价
                close = rqd.get_price(top_group + bottom_group, last_date, date, fields='close')
                # 基准收盘价
                bench_close = rqd.get_price(self.benchmark, last_date, date, fields='close')
                # 股票收益
                profit_series = close.iloc[-1] / close.iloc[0] - 1
                top_profit = profit_series[top_group].mean()
                bottom_profit = profit_series[bottom_group].mean()
                # 基准收益
                bench_profit = bench_close[-1] / bench_close[0] - 1
                df_profit.loc[date] = {'top': top_profit, 'bottom': bottom_profit, 'benchmark': bench_profit}

            last_date = date
            # 选出当天可交易的股票
            universe = self.__select_stock(date)
            factor_df = rqd.get_factor(universe, self.factor, date, date)[lambda x: x > 0]
            # 每档数量
            position_size = int(len(factor_df) / self.group)
            # 清空首档没有停牌的
            if len(top_group) > 0:
                top_suspend = []
                for code in top_group:
                    if rqd.is_suspended(code, date, date).squeeze():
                        top_suspend.append(code)
                top_group = top_suspend
            # 清空末档没有停牌的
            if len(bottom_group) > 0:
                bottom_suspend = []
                for code in bottom_group:
                    if rqd.is_suspended(code, date, date).squeeze():
                        bottom_suspend.append(code)
                bottom_group = bottom_suspend
            # 添加首档
            for code in factor_df.sort_values().index:
                if len(top_group) >= position_size:
                    break
                if code not in top_group:
                    top_group.append(code)
            # 添加末档
            for code in factor_df.sort_values(ascending=False).index:
                if len(bottom_group) >= position_size:
                    break
                if code not in bottom_group:
                    bottom_group.append(code)
        df_profit['top-bottom'] = df_profit['top'] - df_profit['bottom']
        df_cumprod_profit = (df_profit + 1).cumprod()
        df_cumprod_profit.plot()
        plt.show()


if __name__ == '__main__':
    ZeroPortfolioAnalysis(
        'pe_ratio_ttm',
        begin_date='20150101',
        end_date='20200806',
        interval=20,
        group=10
    ).analyze()
