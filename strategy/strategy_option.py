import rqdatac as rqd
from datetime import datetime


class StrategyOption:
    def __init__(self):
        self.options = dict()

    def add_option(self, name, value):
        self.options[name] = value

    @property
    def begin_date(self):
        begin_date = None
        if 'begin_date' in self.options:
            begin_date = self.options['begin_date']
        if begin_date is None or begin_date == '':
            begin_date = '20100101'

        return begin_date

    @property
    def end_date(self):
        end_date = None
        if 'end_date' in self.options:
            end_date = self.options['end_date']
        if end_date is None or end_date == '':
            end_date = datetime.now().strftime('%Y%m%d')

        return end_date
