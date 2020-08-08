import rqdatac as rqd
from pymongo import UpdateOne
from util.database import DB_CONN

rqd.init()


class BasicCrawler:
    def __init__(self):
        pass

    def crawl(self, begin_date=None, end_date=None):
        if begin_date is None and end_date is None:
            return
        # 区间交易日
        dates = rqd.get_trading_dates(begin_date, end_date)
        for date in dates:
            # 当天所有股票
            stocks = rqd.all_instruments(type='CS', date=date)['order_book_id'].tolist()
            update_requests = []
            for i in rqd.instruments(stocks):
                doc = i.__dict__
                # 股票信息与时间无关
                update_requests.append(
                    UpdateOne(
                        {'code': doc['order_book_id']},
                        {'$set': doc},
                        upsert=True
                    )
                )
            if len(update_requests) > 0:
                # bulk_write 批量写入
                # 写入daily数据集合(表) , 不按顺序ordered = False
                update_result = DB_CONN['basic'].bulk_write(update_requests, ordered=False)
                print('保存-%s-%s数据 , 插入:%4d , 更新:%4d'
                      % (date, 'basic', update_result.upserted_count, update_result.modified_count),
                      flush=True)


if __name__ == '__main__':
    bc = BasicCrawler()
    bc.crawl(begin_date='20190501', end_date='20200101')
