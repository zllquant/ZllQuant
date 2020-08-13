from abc import abstractmethod


class BaseAddPositionMethod:
    def __init__(self):
        self.holding_stock_dict = dict()

    def set_holding_stocks(self, holding_stock_dict):
        self.holding_stock_dict = holding_stock_dict

    @abstractmethod
    def update_holding_stock(self, code=None, volume=None, cost=None):
        pass

    @abstractmethod
    def get_position(self, code):
        return 0
