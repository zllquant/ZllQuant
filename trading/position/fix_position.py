from .base_initial_position_method import BaseInitialPositionMethod


class FixPosition(BaseInitialPositionMethod):
    def __init__(self, single_position):
        BaseInitialPositionMethod.__init__(self)
        self.single_position = single_position

    def get_position(self, code):
        return self.single_position
