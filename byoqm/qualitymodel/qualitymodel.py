from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import List

# TODO: find correct terminology for internal node (use ISO)
class Characteristic(ABC):
    @abstractmethod
    def calculate() -> int | float:
        pass


class QualityModel(ABC):
    @abstractmethod
    def insert(
        self,
        parent: Characteristic,
        childen: List[Characteristic],
        aggregations: Callable[..., int | float],
    ):
        """Inserts a new characteristic into the quality model.

        Assumes that `aggregations` is a function with n parameters, where n is the
        number of children.
        """
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def find(self, key: str) -> Characteristic:
        pass
