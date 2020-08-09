import rqdatac as rqd

rqd.init()


class Backtest:
    def __init__(self, strategy_option):
        self.strategy_option = strategy_option

    def run(self):
        begin_date = self.strategy_option.begin_date
        end_date = self.strategy_option.end_date
        # 这是一个类对象
        stock_pool = self.strategy_option.stock_pool
        # 总资金
        capital = self.strategy_option.capital
        # 个股头寸
        single_position = self.strategy_option.single_position
        # 现金
        cash = capital
        if stock_pool is None:
            raise ValueError('没有股票池!')
        adjusted_dates, date_codes_dict = stock_pool.get_stocks()
        # 持仓字典{股票:持仓数量}
        holding_stock_dict = {}
        all_dates = rqd.get_trading_dates(begin_date, end_date)
        last_date = None
        to_sell, to_buy = set(), set()
        # 如果某天发生除权除息,股价会突变,持仓量也会变化
        for date in all_dates:
            if last_date is not None:
                pass

            # 卖出
            if len(to_sell) > 0:
                to_sell_copy = to_sell.copy()
                for code in to_sell_copy:
                    # 没停牌
                    if not rqd.is_suspended(code, date, date).squeeze():
                        sell_price = rqd.get_price(code, date, date, fields='open').values
                        # 卖出的金额
                        sell_amount = sell_price * holding_stock_dict[code]['volume']
                        cash += sell_amount
                        # 要卖的里面删除
                        to_sell.remove(code)
                        # 持仓里面删除
                        del holding_stock_dict[code]

            # 买入
            if len(to_buy) > 0:
                to_buy_copy = to_sell.copy()
                for code in to_buy_copy:
                    if cash < single_position:
                        break
                    # 没停牌,且现金大于个股仓位
                    if not rqd.is_suspended(code, date, date).squeeze():
                        buy_price = rqd.get_price(code, date, date, fields='open').values
                        # 买入的股数
                        buy_volume = int(single_position / buy_price / 100) * 100
                        buy_amount = buy_price * buy_volume
                        cash -= buy_amount
                        # 要买的里面删除
                        to_buy.remove(code)
                        # 持仓里面添加
                        holding_stock_dict[code] = {
                            'buy_price': buy_price,
                            'volume': buy_volume,
                            'cost': buy_amount,
                        }

            # 判断今天是否是调仓日
            if date in adjusted_dates:
                target_stock_today = date_codes_dict[date]
                if last_date is not None:
                    for code in holding_stock_dict.keys():
                        if code not in target_stock_today:
                            to_sell.add(code)
                # 待买股票

            last_date = date
