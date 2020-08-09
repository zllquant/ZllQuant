import os, sys
from strategy.strategy_option import StrategyOption
from trading.back_test import Backtest

"""解析文件"""


class StrategyModule:
    def __init__(self, strategy):
        self.strategy = strategy
        self.strategy_option = StrategyOption()
        self.parse()

    def parse(self):
        strategy_file = sys.path[1] + '\\strategy\\strategies\\' + self.strategy
        if not os.path.exists(strategy_file):
            print("策略文件不存在!")
            return
        with open(strategy_file, 'r', encoding='utf8') as file:
            for line in file:
                if line.startswith('#') or line == '\n':
                    continue
                fields = line.split('=')
                self.strategy_option.add_option(fields[0].strip(), fields[1].strip())

    def backtest(self):
        backtest = Backtest(self.strategy_option)
        backtest.run()


if __name__ == '__main__':
    StrategyModule('low_pe_strategy').backtest()
