from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path


class QualityModel(ABC):
    def __init__(self):
        pass

    def set_src_root(self, root: Path):
        self.src_root = root

    @abstractmethod
    def getDesc(self) -> Dict:
        """
        getDesc returns a dictionary describing the quality model.

        The keys of the dictionary are seen as characteristics of the model, and the
        values aggregation functions.
        """
        pass
