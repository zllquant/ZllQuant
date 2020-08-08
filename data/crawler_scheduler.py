import time
import schedule
from datetime import datetime
from data.daily_crawler import DailyCrawler
from data.basic_crawler import BasicCrawler

def crawl():
    # 行情数据
    dc = DailyCrawler()
    bc = BasicCrawler()
    current_date = datetime.now().strftime('%Y%m%d')
    weekday = datetime.now().strftime('%w')
    if 0 < int(weekday) < 6:
        dc.crawl_index(begin_date=current_date, end_date=current_date)
        dc.crawl_stock(adj=None, begin_date=current_date, end_date=current_date)
        dc.crawl_stock(adj='qfq', begin_date=current_date, end_date=current_date)
        dc.crawl_stock(adj='hfq', begin_date=current_date, end_date=current_date)

    # 基本数据
    bc.crawl()

if __name__ == '__main__':
    schedule.every().day.at('18:00').do(crawl)
    while True:
        schedule.run_pending()
        time.sleep(5)
