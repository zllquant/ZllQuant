from abc import abstractmethod


class BaseStockPool:
    def __init__(self, begin_date, end_date,interval):
        self.begin_date = begin_date
        self.end_date = end_date
        self.interval = interval

    @abstractmethod
    def get_stocks(self):
        return None

    def calculate_profit(self):
        pass
