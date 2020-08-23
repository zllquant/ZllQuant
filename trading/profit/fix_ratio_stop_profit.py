from trading.profit.base_stop_profit import BaseStopProfit


class FixRatioStopProfit(BaseStopProfit):

    def __init__(self, ratio):
        BaseStopProfit.__init__(self)
        self.ratio = ratio

    def update_holding_stocks(self):
        pass

    def is_stop_profit(self, code):
        if code in self.holding_stock_dict:
            holding_stock = self.holding_stock_dict[code]
            cost = holding_stock['cost']
            last_value = holding_stock['last_value']
            profit = last_value / cost - 1
            if profit >= self.ratio:
                print(f"[止盈]: 股票: {code}, 成本:{cost:10.2f}, 市值:{last_value:10.2f}, 收益:{profit:5.2f}")
                return True
        return False
