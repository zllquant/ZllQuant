from datetime import datetime
from factor.pe_factor import PEFactor
import schedule, time

"""定时计算更新所有因子"""


class FactorComputer:
    def __init__(self):
        pass

    def compute_all_factor(self):
        factors = [
            PEFactor(),

        ]

        date = datetime.now().strftime('%Y%m%d')
        for factor in factors:
            factor.compute(begin_date=date, end_date=date)


def compute_after_close():
    weekday = datetime.now().weekday()
    fc = FactorComputer()
    if 0 < weekday < 6:
        fc.compute_all_factor()


if __name__ == '__main__':
    schedule.every().day.at('18:00').do(compute_after_close)
    while True:
        schedule.run_pending()
        time.sleep(5)
        print(datetime.now())