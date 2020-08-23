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
            profit = last_value / cost - 1
            if (profit + self.ratio) <= 0:
                print(f"[止损]: 股票: {code}, 成本:{cost:10.2f}, 市值:{last_value:10.2f}, 收益:{profit:5.2f}")
                return True
        return False
