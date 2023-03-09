from abc import ABC, abstractmethod
from pathlib import Path


class Metric(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self) -> int | float:
        """
        run returns a number that is the measurement of that specific metric.
        """
        pass
