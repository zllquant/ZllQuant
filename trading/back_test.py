import rqdatac as rqd
import pandas as pd

rqd.init()


class Backtest:
    def __init__(self, strategy_option):
        self.strategy_option = strategy_option

    def run(self):
        print("开始回测".center(40, '*'))
        # 这是一个类对象
        stock_pool = self.strategy_option.stock_pool
        if stock_pool is None:
            raise NotImplementedError('没有股票池!')

        # 仓位分配方法
        initial_position_method = self.strategy_option.get_initial_position_method()
        if initial_position_method is None:
            raise NotImplementedError("没有指定仓位分配方法,回测结束!")

        # 起始日期
        begin_date = self.strategy_option.begin_date
        end_date = self.strategy_option.end_date

        # 总资金
        capital = self.strategy_option.capital

        # 现金
        cash = capital

        # 买入卖出信号
        buy_signal = self.strategy_option.buy_signal
        sell_signal = self.strategy_option.sell_signal

        print("获取股票池...")
        adjusted_dates, date_codes_dict = stock_pool.get_stocks()
        print("获取完毕!")
        # 持仓字典{股票:持仓数量}
        holding_stock_dict = {}

        # 待卖,待买,待加仓
        to_sell, to_buy, to_add = set(), set(), set()

        # 这期股票池
        today_target_stock = None
        # 上期股票池
        lastday_target_stock = None

        # 加仓方法
        add_position_method = self.strategy_option.get_add_position_method()
        if add_position_method is not None:
            add_position_method.set_holding_stocks(holding_stock_dict)

        all_dates = rqd.get_trading_dates(begin_date, end_date)
        all_dates = [i.strftime('%Y%m%d') for i in all_dates]
        last_date = None

        for date in all_dates:
            print('日期:%s'.center(95, '*') % date)
            # 如果某天发生除权除息,股价会突变,持仓量也会变化
            if last_date is not None:
                pass

            # 处理卖出
            if len(to_sell) > 0:
                to_sell_copy = to_sell.copy()
                for code in to_sell_copy:
                    # 没停牌
                    if not rqd.is_suspended(code, date, date).squeeze():
                        sell_price = rqd.get_price(code, date, date, fields='open').squeeze()
                        # 卖出的数量
                        volume = holding_stock_dict[code]['volume']
                        # 卖出的金额
                        sell_amount = sell_price * volume
                        cash += sell_amount
                        print(
                            f'[卖出]:日期:{date},股票:{code},成交价:{sell_price:8.2f}:,成交量:{volume:8d},成交额:{sell_amount:10.2f}',
                            flush=True)
                        # 要卖的里面删除
                        to_sell.remove(code)
                        # 持仓里面删除
                        del holding_stock_dict[code]
            print('卖出后现金:%12.2f' % cash, flush=True)

            # 处理买入
            if len(to_buy) > 0:
                to_buy_copy = to_buy.copy()
                for code in to_buy_copy:
                    single_position = initial_position_method.get_position(code)
                    if cash < single_position:
                        print("可用现金不足,不再买入,现金:%10.2f,头寸:%10.2f" %
                              (cash, single_position))
                        break
                    # 没停牌,且现金大于个股仓位
                    if not rqd.is_suspended(code, date, date).squeeze():
                        # 名称
                        stock_name = rqd.instruments(code).symbol
                        # 行业
                        industry = rqd.shenwan_instrument_industry(code)[1]
                        buy_price = rqd.get_price(code, date, date, fields='open').squeeze()
                        # 买入的股数
                        buy_volume = int(single_position / buy_price / 100) * 100
                        buy_amount = buy_price * buy_volume
                        cash -= buy_amount
                        print('[买入]: 代码: %s,成交价:%8.2f:,成交量:%8d,成交额:%12.2f,名称:%5s,行业:%5s,' %
                              (code, buy_price, buy_volume, buy_amount, stock_name, industry), flush=True)
                        # 持仓里面添加
                        holding_stock_dict[code] = {
                            'buy_price': buy_price,
                            'volume': buy_volume,
                            'cost': buy_amount
                        }
            print('买入后现金:%12.2f' % cash, flush=True)

            # 处理加仓
            if len(to_add) > 0:
                to_add_copy = to_add.copy()
                for code in to_add_copy:
                    single_position = add_position_method.get_position(code)
                    if cash < single_position:
                        print("可用现金不足,不再买入,现金:%10.2f,头寸:%10.2f" %
                              (cash, single_position))
                        break
                    # 没停牌,且现金大于个股仓位
                    if not rqd.is_suspended(code, date, date).squeeze():
                        # 名称
                        stock_name = rqd.instruments(code).symbol
                        # 行业
                        industry = rqd.shenwan_instrument_industry(code)[1]
                        buy_price = rqd.get_price(code, date, date, fields='open').squeeze()
                        # 买入的股数
                        buy_volume = int(single_position / buy_price / 100) * 100
                        buy_amount = buy_price * buy_volume
                        cash -= buy_amount
                        add_position_method.update_holding_stock(
                            code=code, volume=buy_volume, cost=buy_amount
                        )
                        print('[加仓]: 代码: %s,成交价:%8.2f:,成交量:%8d,成交额:%12.2f,名称:%5s,行业:%5s,' %
                              (code, buy_price, buy_volume, buy_amount, stock_name, industry), flush=True)

            print('加仓后现金:%12.2f' % cash, flush=True)

            # 判断今天是否是调仓日
            if date in adjusted_dates:
                today_target_stock = date_codes_dict[date]
                if lastday_target_stock is not None:
                    for code in lastday_target_stock:
                        if code not in today_target_stock and code in holding_stock_dict:
                            to_sell.add(code)
                lastday_target_stock = today_target_stock

            # 每日判断是否出现卖出信号
            if sell_signal is not None:
                # 已经持仓的是否要卖出
                for code in holding_stock_dict:
                    if sell_signal.is_match(code, date):
                        to_sell.add(code)

            # 每日判断是否出现买入信号
            to_buy.clear()
            if buy_signal is not None:
                for code in today_target_stock:
                    if code not in holding_stock_dict and buy_signal.is_match(code, date):
                        to_buy.add(code)

            # 加仓信号
            to_add.clear()
            if buy_signal is not None:
                for code in holding_stock_dict:
                    if buy_signal.is_match(code, date):
                        to_add.add(code)

            # 打印待买,待卖列表
            print('今日待买:', to_buy)
            print('今日待卖:', to_sell)
            print('今日持仓:', '\n', pd.DataFrame(holding_stock_dict).T)
            last_date = date


if __name__ == '__main__':
    pass
