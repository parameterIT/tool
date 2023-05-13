from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path


class QualityModel(ABC):
    def __init__(self):
        pass

    def set_results(self, results: Path):
        self.results = results

    @abstractmethod
    def get_desc(self) -> Dict:
        """
        get_desc returns a dictionary describing the quality model.

        The first level of the dictionary should be two keys:
        - metrics
        - aggregations

        The value of metrics should be a nested dictionary where key-value pairs are
        metric name-path to metric executable pairs.

        The value of aggregations should be a nested dictionary where key-value pairs
        are aggregation name-aggregation function reference pairs
        """
        pass
