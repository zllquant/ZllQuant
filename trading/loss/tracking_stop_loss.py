from trading.loss.base_stop_loss import BaseStopLoss


class TrackingStopLoss(BaseStopLoss):

    def __init__(self, ratio):
        BaseStopLoss.__init__(self)
        self.ratio = ratio

    def update_holding_stocks(self):
        for code in self.holding_stock_dict:
            holding_stock = self.holding_stock_dict[code]
            last_value = holding_stock['last_value']
            if 'highest_value' not in holding_stock or \
                    holding_stock['highest_value'] < last_value:
                holding_stock['hightest_value'] = last_value

    def is_stop_loss(self, code):
        if code in self.holding_stock_dict:
            holding_stock = self.holding_stock_dict[code]
            last_value = holding_stock['last_value']
            highest_value = holding_stock['highest_value']
            if last_value >= highest_value:
                return False
            profit = last_value / highest_value - 1
            return (profit + self.ratio) <= 0

        return False
