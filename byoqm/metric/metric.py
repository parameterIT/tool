from abc import ABC, abstractmethod
from pathlib import Path


class Metric(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self) -> int | float:
        pass
