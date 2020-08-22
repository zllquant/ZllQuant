from abc import abstractmethod


class BaseStopLoss:
    def __init__(self):
        self.holding_stock_dict = dict()

    def set_holding_stocks(self, holding_stock_dict):
        self.holding_stock_dict = holding_stock_dict

    @abstractmethod
    def update_holding_stocks(self):
        pass

    @abstractmethod
    def is_stop_loss(self, code):
        return False
