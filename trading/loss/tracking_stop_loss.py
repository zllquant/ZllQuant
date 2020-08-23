from trading.loss.base_stop_loss import BaseStopLoss


class TrackingStopLoss(BaseStopLoss):

    def __init__(self, ratio):
        BaseStopLoss.__init__(self)
        self.ratio = ratio

    def update_holding_stocks(self):
        for code in self.holding_stock_dict:
            holding_stock = self.holding_stock_dict[code]
            last_value = holding_stock['last_value']
            cost = holding_stock['cost']
            if 'highest_value' not in holding_stock:
                self.holding_stock_dict[code]['highest_value'] = max(cost, last_value)
            elif holding_stock['highest_value'] < last_value:
                self.holding_stock_dict[code]['highest_value'] = last_value

    def is_stop_loss(self, code):
        if code in self.holding_stock_dict:
            holding_stock = self.holding_stock_dict[code]
            cost = holding_stock['cost']
            last_value = holding_stock['last_value']
            highest_value = holding_stock['highest_value']
            profit_loss = last_value / highest_value - 1
            profit = last_value / cost - 1
            if (profit_loss + self.ratio) <= 0:
                print(f"[跟踪止损]: 股票: {code}, 最高:{highest_value:10.2f}, 市值:{last_value:10.2f}, 收益:{profit:5.2f}")
                return True
        return False
