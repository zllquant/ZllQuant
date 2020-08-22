from trading.loss.base_stop_loss import BaseStopLoss


class FixRatioStopLoss(BaseStopLoss):

    def __init__(self, ratio):
        BaseStopLoss.__init__(self)
        self.ratio = ratio

    def update_holding_stocks(self):
        pass

    def is_stop_loss(self, code):
        if code in self.holding_stock_dict:
            cost = self.holding_stock_dict[code]['cost']
            last_value = self.holding_stock_dict[code]['last_value']
            if cost < last_value:
                return False
            profit = last_value / cost - 1
            return (profit + self.ratio) <= 0
        return False
