from .base_add_position_method import BaseAddPositionMethod


class FixRatioAddPositionMethod(BaseAddPositionMethod):
    def __init__(self, ratio):
        BaseAddPositionMethod.__init__(self)
        self.ratio = ratio

    def update_holding_stock(self, code=None, volume=None, cost=None):
        # 原持仓情况
        holding_stock = self.holding_stock_dict[code]
        self.holding_stock_dict[code].update(
            {
                'cost': holding_stock['cost'] + cost,
                'added': True,
                'volume': holding_stock['volume'] + volume,
                'last_value': holding_stock['last_value'] + cost
            }
        )

    def get_position(self, code):
        # 有字段说明已经加仓,不再加仓
        if code in self.holding_stock_dict and \
                'added' not in self.holding_stock_dict[code]:
            position = self.ratio * self.holding_stock_dict[code]['cost']
            return position
