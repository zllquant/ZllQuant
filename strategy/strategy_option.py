import rqdatac as rqd
from datetime import datetime
from strategy.stockpool.stock_pool_factory import StockPoolFactory
from trading.signal.signal_factory import SignalFactory
from trading.position.position_factory import PositionFactory

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
            return '20100101'

        return begin_date

    @property
    def end_date(self):
        end_date = self.options.get('end_date', None)
        if end_date is None or end_date == '':
            return datetime.now().strftime('%Y%m%d')

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
    def buy_signal(self):
        if 'buy_signal' in self.options:
            return SignalFactory.get_signal(self.options['buy_signal'])

    @property
    def sell_signal(self):
        if 'sell_signal' in self.options:
            return SignalFactory.get_signal(self.options['sell_signal'])

    def get_initial_position_method(self):
        position_method = None
        if 'initial_position_method' in self.options:
            name = self.options['initial_position_method']
            return PositionFactory.get_position_method(name, self.options)
        return position_method

    def get_add_position_method(self):
        add_position_method = None
        if 'add_position_method' in self.options:
            name = self.options['add_position_method']
            return PositionFactory.get_position_method(name, self.options)
        return add_position_method
