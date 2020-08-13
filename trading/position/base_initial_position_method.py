from abc import abstractmethod


class BaseInitialPositionMethod:
    def __init__(self):
        pass

    @abstractmethod
    def get_position(self, code):
        return 0
