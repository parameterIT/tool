from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import List
from metric import Metric


class Characteristic(ABC):
    @abstractmethod
    def measure() -> int | float:
        pass

class QualityModel(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def insert(
        self,
        parent: Characteristic,
        child: Characteristic | Metric
        ):
        """Inserts a new characteristic into the quality model.

        Aggregation is a function with the signature: f(int | float list, int | float list) -> int | float
        """
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def find(self, key: str) -> Characteristic:
        pass

    @abstractmethod
    def measure(self):
        pass