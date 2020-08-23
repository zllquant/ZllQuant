from trading.loss.fix_ratio_stop_loss import FixRatioStopLoss
from trading.loss.tracking_stop_loss import TrackingStopLoss


class StopLossFactory:
    @staticmethod
    def get_stop_loss(name, options):
        if name == 'fix_ratio':
            if 'stop_loss_ratio' in options:
                return FixRatioStopLoss(float(options['stop_loss_ratio']))
        elif name == 'tracking_stop_loss':
            if 'stop_loss_ratio' in options:
                return TrackingStopLoss(float(options['stop_loss_ratio']))
