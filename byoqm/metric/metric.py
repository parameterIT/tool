from abc import ABC, abstractmethod


class Metric(ABC):
    @abstractmethod
    def measure(self) -> int | float:
        pass
