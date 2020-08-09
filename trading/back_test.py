class Backtest:
    def __init__(self, strategy_option):
        self.strategy_option = strategy_option

    def run(self):
        begin_date = self.strategy_option.begin_date
        end_date = self.strategy_option.end_date
        print(begin_date)
        print(end_date)
