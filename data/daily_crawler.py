# -*- coding:utf-8 -*-
from util.database import DB_CONN
import tushare as ts
from pymongo import UpdateOne

pro = ts.pro_api()


class DailyCrawler:

    def __init__(self):
        pass

    # self 根本没有用到,可以变成静态方法
    def crawl_index(self, begin_date=None, end_date=None):
        """
        抓取指数数据
        :param begin_date:
        :param end_date:
        :return:
        """
        codes = ['000001.SH', '000300.SH', '399001.SZ', '399005.SZ', '399006.SZ', '000905.SH']
        for code in codes:
            df_daily = pro.index_daily(ts_code=code, start_date=begin_date, end_date=end_date)
            self.save_database(df_daily, code, adj=None)

    def crawl_stock(self, adj=None, begin_date=None, end_date=None):
        """

        :param adj:
        :param begin_date:
        :param end_date:
        :return:
        """
        codelist = pro.stock_basic(exchange='', list_status='L', fields='ts_code')['ts_code'].tolist()
        for code in codelist:
            df_daily = ts.pro_bar(ts_code=code, adj=adj, start_date=begin_date, end_date=end_date,
                                  factors=['tor', 'vr'])
            self.save_database(df_daily, code, adj)

    def save_database(self, df_daily, code, adj):
        """
        存入数据库
        :param df_daily: dataframe
        :param code:
        :param adj:
        :return:
        """
        # 日期升序
        df_daily.sort_values(by='trade_date', inplace=True)
        df_daily.rename(columns={'ts_code': 'code', 'trade_date': 'date'}, inplace=True)
        df_daily['code'] = df_daily['code'].map(
            lambda x: x.replace('SH', 'XSHG') if x[-1] == 'H' else x.replace('SZ', 'XSHE'))
        updates_requests = []
        # 每一行数据转成字典
        for index in df_daily.index:
            doc = dict(df_daily.loc[index])
            # flush=True , 只要有日志就输出,没有间隔
            # print(doc, flush=True)
            # 这里不用insert避免重复数据,所以用更新
            updates_requests.append(
                # filter : 更新哪一条
                # $set : 更新的值
                # upsert : 找到就更新,没找到就插入
                # 记得在黑窗加索引,查询比较快
                UpdateOne(
                    {'code': doc['code'], 'date': doc['date']},
                    {'$set': doc},
                    upsert=True
                )
            )

        # 保证不为空
        if len(updates_requests) > 0:
            collection_name = 'daily' if adj is None else 'daily_' + adj
            # bulk_write 批量写入
            # 写入daily数据集合(表) , 不按顺序ordered = False
            update_result = DB_CONN[collection_name].bulk_write(updates_requests, ordered=False)
            print('保存-%s-%s数据 , 插入:%4d , 更新:%4d'
                  % (code, collection_name, update_result.upserted_count, update_result.modified_count),
                  flush=True)


if __name__ == '__main__':
    dc = DailyCrawler()
    begin_date = '20200101'
    end_date = '20200806'
    # dc.crawl_index(begin_date=begin_date, end_date=end_date)
    dc.crawl_stock('qfq', begin_date, end_date)
    # dc.crawl_stock('hfq',begin_date,end_date)
    # dc.crawl_stock(begin_date,end_date,adj=None)
