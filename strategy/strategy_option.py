import rqdatac as rqd
from datetime import datetime
from strategy.stockpool.stock_pool_factory import StockPoolFactory
from trading.signal.signal_factory import SignalFactory

"""增加参数,获取参数类"""


class StrategyOption:
    def __init__(self):
        self.options = dict()

    def add_option(self, name, value):
        self.options[name] = value

    @property
    def begin_date(self):
        begin_date = self.options.get('begin_date', None)
        if begin_date is None or begin_date == '':
            begin_date = '20100101'

        return begin_date

    @property
    def end_date(self):
        end_date = self.options.get('end_date', None)
        if end_date is None or end_date == '':
            end_date = datetime.now().strftime('%Y%m%d')

        return end_date

    @property
    def stock_pool(self):
        stock_pool = self.options.get('stock_pool', None)
        if stock_pool is not None:
            interval = self.options.get('stock_pool_rebalance_dates', None)
            if interval is not None:
                stock_pool = StockPoolFactory.get_stock_pool(
                    self.options['stock_pool'],
                    self.begin_date,
                    self.end_date,
                    int(interval)
                )

        return stock_pool

    @property
    def capital(self):
        capital = self.options.get('capital', None)
        if capital is None or capital == '':
            capital = 1e7
        return float(capital)

    @property
    def single_position(self):
        single_position = self.options.get('single_position', None)
        if single_position is None or single_position == '':
            single_position = 2e5
        return int(single_position)

    @property
    def buy_signal(self):
        buy_signal = None
        if 'buy_signal' in self.options:
            return SignalFactory.get_signal(self.options['buy_signal'])
        return buy_signal
