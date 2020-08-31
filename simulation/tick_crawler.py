import rqdatac as rqd
import pandas as pd
import tushare as ts
import time
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

rqd.init()
codes = ['000001.XSHE', '000002.XSHE', '000006.XSHE', '000004.XSHE']

# for code in codes:
#     tick = rqd.get_price(code, '20200825', '20200825', frequency='tick').reset_index().iloc[1000:2000]
#     tick['datetime'] = tick['datetime'].apply(lambda x: x.strftime('%H:%M:%S'))
#     tick['trading_date'] = tick['trading_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
#     tick['code'] = code
#     for _, i in tick.iterrows():
#         print(dict(i))

for _ in range(100):
    for code in ['601788', '300750', '300015', '601318', '300059']:
        tick = ts.get_realtime_quotes(code).squeeze().to_dict()
        print(tick)
    time.sleep(3)
