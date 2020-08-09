from util.database import DB_CONN
from abc import abstractmethod


class BaseSignal:
    def __init__(self, name):
        self.name = name
        self.collection = DB_CONN[name]

    @abstractmethod
    def compute(self, begin_date=None, end_date=None):
        pass

    def is_match(self, code, date):
        signal = self.collection.find_one(
            {'code': code, 'date': date}
        )

        return signal is not None
