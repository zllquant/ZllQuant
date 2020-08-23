from datetime import datetime
from strategy.stockpool.stock_pool_factory import StockPoolFactory
from trading.profit.stop_profit_factory import StopProfitFactory
from trading.signal.signal_factory import SignalFactory
from trading.position.position_factory import PositionFactory
from trading.loss.stop_loss_factory import StopLossFactory

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
    def benchmark(self):
        benchmark = self.options.get('benchmark', None)
        if benchmark is None or benchmark == '':
            benchmark = '000300.XSHG'
        return benchmark

    @property
    def buy_signal(self):
        if 'buy_signal' in self.options:
            return SignalFactory.get_signal(self.options['buy_signal'])

    @property
    def sell_signal(self):
        if 'sell_signal' in self.options:
            return SignalFactory.get_signal(self.options['sell_signal'])

    @property
    def initial_position_method(self):
        if 'initial_position_method' in self.options:
            name = self.options['initial_position_method']
            return PositionFactory.get_position_method(name, self.options)

    @property
    def add_position_method(self):
        if 'add_position_method' in self.options:
            name = self.options['add_position_method']
            return PositionFactory.get_position_method(name, self.options)

    @property
    def stop_loss(self):
        if 'stop_loss' in self.options:
            name = self.options['stop_loss']
            return StopLossFactory.get_stop_loss(name, self.options)

    @property
    def stop_profit(self):
        if 'stop_profit' in self.options:
            name = self.options['stop_profit']
            return StopProfitFactory.get_stop_profit(name, self.options)
