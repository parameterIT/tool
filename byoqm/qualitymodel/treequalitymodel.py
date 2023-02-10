from abc import ABC, abstractmethod
from ast import List
from typing import Callable
from qualitymodel import Characteristic, QualityModel


class Node(Characteristic):
    def __init__(self, name: str, parent: Node, weights: List[int | float]):
        self.name = name
        self.parent = parent
        self.children = []
        self.weights = weights

    def measure(self):
        measurement = None
        for c in self.children:
            measurement += c.measure()


class TreeQualityModel(QualityModel):
    def __init__(self):
        self.root = Node("root", None, [])

    def insert(self, children, parent, weights: List[float | int]):
        self.find(parent).append(children)

    def keys():
        pass

    def find():
        pass

    def measure():
        pass
