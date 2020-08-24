import rqdatac as rqd
import pandas as pd
import matplotlib.pyplot as plt


class BackTest:
    def __init__(self, strategy_option):
        plt.style.use('ggplot')
        rqd.init()
        self.strategy_option = strategy_option

    def get_all_code_price(self, date, holding_stock_dict, to_buy, to_sell, to_add):
        all_code_set = set()
        for code in holding_stock_dict.keys():
            all_code_set.add(code)
        all_code_set = all_code_set.union(to_sell).union(to_buy).union(to_add)
        if len(all_code_set) == 0:
            return None
        df_price = rqd.get_price(all_code_set, date, date, fields=['open', 'close'], expect_df=True).droplevel(1)
        is_suspend = rqd.is_suspended(all_code_set, date, date).squeeze()
        df_price['is_suspended'] = is_suspend

        return df_price

    def save_and_print_trades(self, side, amount, price, volume, code, date, trades):
        print(
            f'[{side}]: 股票:{code},成交价:{price:8.2f}:,成交量:{volume:8d},成交额:{amount:10.2f}',
            flush=True)
        trades.append({'日期': date, '代码': code, '方向': side, '成交价': price, '成交量': volume,
                       '成交额': amount})

    def run(self):
        print("开始回测".center(40, '*'))
        # ====================获取必要参数====================
        # 股票池,这是一个类对象
        stock_pool = self.strategy_option.stock_pool
        if stock_pool is None:
            raise NotImplementedError('没有股票池!')

        # 仓位分配方法
        initial_position_method = self.strategy_option.initial_position_method
        if initial_position_method is None:
            raise NotImplementedError("没有指定仓位分配方法,回测结束!")

        print("获取股票池...")
        adjusted_dates, date_codes_dict = stock_pool.get_stocks()
        print("获取完毕!")

        # 起止日期
        begin_date = self.strategy_option.begin_date
        end_date = self.strategy_option.end_date
        # 初始总资金
        initial_capital = self.strategy_option.capital
        # 比较基准
        benchmark = self.strategy_option.benchmark
        # 买入卖出信号
        buy_signal = self.strategy_option.buy_signal
        sell_signal = self.strategy_option.sell_signal
        # 加仓方法
        add_position_method = self.strategy_option.add_position_method
        # 止损策略
        stop_loss = self.strategy_option.stop_loss
        # 止盈策略
        stop_profit = self.strategy_option.stop_profit

        # ===================初始化变量====================
        # 初始现金
        cash = initial_capital
        # 持仓字典{股票:持仓数量}
        holding_stock_dict = {}
        # 待卖,待买,待加仓
        to_sell, to_buy, to_add = set(), set(), set()
        # 这期股票池
        current_target_stock = None
        # 上期股票池
        last_target_stock = None
        # 交易流水
        trades = []
        # 每日净值
        profit_df = pd.DataFrame(columns=['net_value', benchmark])

        # 添加持仓字典属性
        if add_position_method is not None:
            add_position_method.set_holding_stocks(holding_stock_dict)
        if stop_loss is not None:
            stop_loss.set_holding_stocks(holding_stock_dict)
        if stop_profit is not None:
            stop_profit.set_holding_stocks(holding_stock_dict)

        # 交易日历
        all_dates = rqd.get_trading_dates(begin_date, end_date)
        all_dates = [i.strftime('%Y%m%d') for i in all_dates]
        # 基准初始价格
        initial_benchmark = rqd.get_price(benchmark, all_dates[0], all_dates[0], fields='close').squeeze()
        last_date = None
        for date in all_dates:
            print('日期:%s'.center(70, '*') % date)
            # 获得所有股票的行情和停牌信息
            df_price = self.get_all_code_price(date, holding_stock_dict, to_buy, to_sell, to_add)
            # 如果某天发生除权除息,股价会突变,持仓量也会变化
            if last_date is not None:
                pass

            # 处理卖出
            if len(to_sell) > 0:
                to_sell_copy = to_sell.copy()
                for code in to_sell_copy:
                    # 没停牌
                    if not df_price.loc[code, 'is_suspended']:
                        sell_price = df_price.loc[code, 'open']
                        # 卖出的数量
                        sell_volume = holding_stock_dict[code]['volume']
                        # 卖出的金额
                        sell_amount = sell_price * sell_volume
                        cash += sell_amount
                        self.save_and_print_trades('卖出', sell_amount, sell_price, sell_volume, code, date, trades)
                        # 要卖的里面删除
                        to_sell.remove(code)
                        # 持仓里面删除
                        del holding_stock_dict[code]
            else:
                print('[卖出]: 无')
            print('卖出后现金:%12.2f' % cash, end='\n\n', flush=True)

            # 处理买入
            if len(to_buy) > 0:
                for code in to_buy:
                    single_position = initial_position_method.get_position(code)
                    if cash < single_position:
                        print("可用现金不足,不再买入,现金:%10.2f,头寸:%10.2f" %
                              (cash, single_position))
                        break
                    # 没停牌,且现金大于个股仓位
                    if not df_price.loc[code, 'is_suspended']:
                        buy_price = df_price.loc[code, 'open']
                        # 买入的股数
                        buy_volume = int(single_position / buy_price / 100) * 100
                        buy_amount = buy_price * buy_volume
                        cash -= buy_amount
                        self.save_and_print_trades('买入', buy_amount, buy_price, buy_volume, code, date, trades)
                        # 持仓里面添加
                        holding_stock_dict[code] = {
                            'buy_price': buy_price,
                            'volume': buy_volume,
                            'cost': buy_amount
                        }
            else:
                print('[买入]: 无')
            print('买入后现金:%12.2f' % cash, end='\n\n', flush=True)

            # 处理加仓
            if len(to_add) > 0:
                for code in to_add:
                    single_position = add_position_method.get_position(code)
                    if single_position is None:
                        print(f"{code}加仓失败!")
                        continue
                    if cash < single_position:
                        print("可用现金不足,不再买入,现金:%10.2f,头寸:%10.2f" %
                              (cash, single_position))
                        break
                    # 没停牌,且现金大于个股仓位
                    if not df_price.loc[code, 'is_suspended']:
                        buy_price = df_price.loc[code, 'open']
                        # 买入的股数
                        buy_volume = int(single_position / buy_price / 100) * 100
                        buy_amount = buy_price * buy_volume
                        cash -= buy_amount
                        self.save_and_print_trades('加仓', buy_amount, buy_price, buy_volume, code, date, trades)
                        # 更新现有持仓
                        add_position_method.update_holding_stock(
                            code=code, volume=buy_volume, cost=buy_amount
                        )
            else:
                print('[加仓]: 无')
            print('加仓后现金:%12.2f' % cash, end='\n\n', flush=True)

            # 判断今天是否是调仓日
            if date in adjusted_dates:
                current_target_stock = date_codes_dict[date]
                if last_target_stock is not None:
                    for code in holding_stock_dict:
                        if code not in current_target_stock:
                            to_sell.add(code)
                last_target_stock = current_target_stock

            # 判断持仓股是否出现卖出信号
            if sell_signal is not None:
                for code in holding_stock_dict:
                    if sell_signal.is_match(code, date):
                        to_sell.add(code)

            # 判断未买入的股票是否出现买入信号
            to_buy.clear()
            if buy_signal is not None:
                for code in current_target_stock:
                    if code not in holding_stock_dict and buy_signal.is_match(code, date):
                        to_buy.add(code)

            # 加仓
            to_add.clear()
            if buy_signal is not None and add_position_method is not None:
                for code in holding_stock_dict:
                    if buy_signal.is_match(code, date):
                        to_add.add(code)

            # 更新持仓股的市值
            codes = list(holding_stock_dict.keys())
            # 持仓股总市值
            total_value = 0
            if len(codes) > 0:
                df_holding_daily = df_price.loc[codes, 'close']
                for code in df_holding_daily.index:
                    close = df_holding_daily.loc[code]
                    value = close * holding_stock_dict[code]['volume']
                    holding_stock_dict[code]['last_value'] = value
                    total_value += value

            # 止损
            if stop_loss is not None:
                # 更新持仓股信息
                stop_loss.update_holding_stocks()
                for code in holding_stock_dict:
                    if stop_loss.is_stop_loss(code):
                        to_sell.add(code)

            # 止盈
            if stop_profit is not None:
                # 更新持仓股信息
                # stop_loss.update_holding_stocks()
                for code in holding_stock_dict:
                    if stop_profit.is_stop_profit(code):
                        to_sell.add(code)

            # 当期总资产
            current_capital = cash + total_value
            # 策略净值
            net_value = current_capital / initial_capital
            # 基准净值
            benchmark_close = rqd.get_price(benchmark, date, date, fields='close').squeeze()
            profit_df.loc[date] = {'net_value': net_value, benchmark: benchmark_close / initial_benchmark}

            # 打印待买,待卖列表
            print('待买:', to_buy)
            print('待卖:', to_sell)
            print('加仓:', to_add)
            print()
            print(
                f'持仓数:{len(holding_stock_dict):3d}, 净值:{net_value:5.2f}, 现金:{cash:12.2f}, 总资产:{current_capital:13.2f}',
                end='\n\n')
            last_date = date

        # trades = pd.DataFrame(trades)
        # trades.to_csv(r'trades.csv')
        profit_df.plot(figsize=(8, 4))
        plt.show()


if __name__ == '__main__':
    pass
