from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_figure(self, data, key):
        """
        get_figure returns a bokeh figure.
        """
        pass