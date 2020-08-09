import sys
from strategy.strategy_module import StrategyModule

"""
python backtest.py low_pe_strategy
"""

if __name__ == '__main__':
    arg_size = len(sys.argv)

    if arg_size == 2:
        StrategyModule(sys.argv[1]).backtest()
    else:
        print("执行: python backtest.py strategy_name")
