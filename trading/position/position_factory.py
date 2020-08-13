from trading.position.fix_position import FixPosition
from trading.position.fix_ratio_add_position_method import FixRatioAddPositionMethod

class PositionFactory:
    @staticmethod
    def get_position_method(name, options):
        if name == 'fix_position':
            if 'single_position' in options:
                single_position = int(options['single_position'])
                return FixPosition(single_position)
            else:
                return None
        elif name == 'fix_ratio_position':
            if 'add_position_ratio' in options:
                add_position_ratio = float(options['add_position_ratio'])
                return FixRatioAddPositionMethod(add_position_ratio)
            else:
                return None
