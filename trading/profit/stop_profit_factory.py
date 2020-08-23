from trading.profit.fix_ratio_stop_profit import FixRatioStopProfit
from trading.profit.drawback_stop_profit import DrawbackStopProfit


class StopProfitFactory:
    @staticmethod
    def get_stop_profit(name, options):
        if name == 'fix_ratio':
            if 'stop_profit_ratio' in options:
                return FixRatioStopProfit(float(options['stop_profit_ratio']))

        elif name == 'drawback_stop_profit':
            if 'stop_profit_ratio' in options:
                if 'stop_profit_drawback' in options:
                    return DrawbackStopProfit(float(options['stop_profit_ratio']),
                                              float(options['stop_profit_drawback']))
