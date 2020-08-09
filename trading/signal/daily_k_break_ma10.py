from trading.signal.base_signal import BaseSignal
from datetime import datetime, timedelta
import rqdatac as rqd
from util.selectstock import filter_stock_pool
from pymongo import UpdateOne

rqd.init()


class DailyUpBreakMa10(BaseSignal):
    def __init__(self):
        BaseSignal.__init__(self, 'daily_up_break_ma10')

    def compute(self, begin_date=None, end_date=None):
        begin_date = datetime.strptime(begin_date, '%Y%m%d') - timedelta(days=20)
        all_filter_codes = filter_stock_pool(begin_date)
        for code in all_filter_codes:
            df_daily = rqd.get_price(code, begin_date, end_date)
            df_daily['ma10'] = df_daily['close'].rolling(10).mean()
            df_daily['delta'] = df_daily['close'] - df_daily['ma10']
            df_daily['delta_pre'] = df_daily['delta'].shift(1)
            df_daily = df_daily[(df_daily['delta'] > 0) & (df_daily['delta_pre'] < 0)]
            update_requests = []
            for date in df_daily.index:
                date = date.strftime('%Y%m%d')
                update_requests.append(
                    UpdateOne(
                        {'code': code, 'date': date},
                        {'$set': {'code': code, 'date': date}},
                        upsert=True
                    )
                )
            if len(update_requests) > 0:
                self.collection.bulk_write(update_requests, ordered=False)


if __name__ == '__main__':
    DailyUpBreakMa10().compute('20200101', '20200505')