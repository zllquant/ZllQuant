from trading.signal.daily_k_break_ma10 import DailyUpBreakMa10


class SignalFactory:
    @staticmethod
    def get_signal(name):
        if name == 'daily_up_break_ma10':
            return DailyUpBreakMa10()
