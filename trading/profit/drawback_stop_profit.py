from trading.profit.base_stop_profit import BaseStopProfit


class DrawbackStopProfit(BaseStopProfit):

    def __init__(self, ratio, drawback):
        BaseStopProfit.__init__(self)
        self.ratio = ratio
        self.drawback = drawback

    def update_holding_stocks(self):
        for code in self.holding_stock_dict:
            holding_stock = self.holding_stock_dict[code]
            last_value = holding_stock['last_value']
            cost = holding_stock['cost']
            if 'highest_value' not in holding_stock:
                self.holding_stock_dict[code]['highest_value'] = max(cost, last_value)
            elif holding_stock['highest_value'] < last_value:
                self.holding_stock_dict[code]['highest_value'] = last_value

    def is_stop_profit(self, code):
        if code in self.holding_stock_dict:
            holding_stock = self.holding_stock_dict[code]
            if 'highest_value' in holding_stock:
                highest_value = holding_stock['highest_value']
                cost = holding_stock['cost']
                last_value = holding_stock['last_value']
                profit_highest = highest_value / cost - 1
                profit_drawback = last_value / highest_value - 1
                profit = last_value / cost - 1
                if (profit_highest >= self.ratio) and (profit_drawback + self.drawback) <= 0:
                    print(
                        f"[回撤止盈]: 股票: {code}, 成本:{cost:10.2f}, 市值:{last_value:10.2f}, "
                        f"最高:{highest_value:10.2f}, 回撤:{profit_drawback:5.2f}, 收益:{profit:5.2f}")
                    return True
        return False
