from strategy.stockpool.base_stock_pool import BaseStockPool
from factor.factor_module import FactorModule
import rqdatac as rqd
from util.selectstock import filter_stock_pool

rqd.init()


class LowPeStockPool(BaseStockPool):
    def get_stocks(self):
        all_dates = rqd.get_trading_dates(self.begin_date, self.end_date)
        adjusted_dates = []
        date_codes_dict = {}
        # 获取因子数据
        fm = FactorModule()
        last_date = None
        stocklist = []
        for index in range(0, len(all_dates), self.interval):
            date = all_dates[index]
            adjusted_dates.append(date)
            # 先保存现在持有的股票中的停牌股
            if len(stocklist) > 0:
                stocks_suspend = []
                for code in stocklist:
                    if rqd.is_suspended(code, date, date).squeeze():
                        stocks_suspend.append(code)
                stocklist = stocks_suspend

            # 去除了今天停牌、ST、上市不满60
            universe = filter_stock_pool(date)
            df_factor = fm.get_factor_one_day(universe, 'pe_ratio_ttm', date)
            for code in df_factor[df_factor > 0].sort_values().index:
                if len(stocklist) >= 100:
                    break
                if code not in stocklist:
                    stocklist.append(code)
            date_codes_dict[date] = stocklist

        return adjusted_dates, date_codes_dict
