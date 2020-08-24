import rqdatac as rqd
import pandas as pd
import tushare as ts
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

rqd.init()

# tick = rqd.get_price('000001.XSHE', '20200824', '20200824', frequency='tick')
# print(tick)

tick = ts.get_realtime_quotes('000001')
print(tick)

