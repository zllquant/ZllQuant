from strategy.stockpool.base_stock_pool import BaseStockPool
from factor.factor_module import FactorModule
import rqdatac as rqd
from util.selectstock import filter_stock_pool

rqd.init()


class LowPeStockPool(BaseStockPool):
    def get_stocks(self):
        all_dates = rqd.get_trading_dates(self.begin_date, self.end_date)
        all_dates = [i.strftime('%Y%m%d') for i in all_dates]
        adjusted_dates = []
        date_codes_dict = {}
        # 获取因子数据
        fm = FactorModule()
        for index in range(0, len(all_dates), self.interval):
            date = all_dates[index]
            print('正在获取:', date)
            adjusted_dates.append(date)
            # # 先保存现在持有的股票中的停牌股
            # if len(stocklist) > 0:
            #     stocks_suspend = []
            #     for code in stocklist:
            #         if rqd.is_suspended(code, date, date).squeeze():
            #             stocks_suspend.append(code)
            #     stocklist = stocks_suspend

            # 去除了今天停牌、ST、上市不满60
            universe = filter_stock_pool(date)
            # 用的是米筐的数据
            df_factor = fm.get_factor_one_day(universe, 'pe_ratio_ttm', date)
            stocklist = df_factor[df_factor > 0].nsmallest(100).index.tolist()
            date_codes_dict[date] = stocklist
        return adjusted_dates, date_codes_dict
