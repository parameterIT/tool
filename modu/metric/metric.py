from abc import ABC, abstractmethod
from pathlib import Path

from modu.metric.result import Result


class Metric(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self) -> Result:
        """
        run returns a number that is the measurement of that specific metric.
        """
        pass
