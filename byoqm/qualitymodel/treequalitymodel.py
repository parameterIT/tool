from typing import List
from byoqm.qualitymodel.qualitymodel import Characteristic, QualityModel


class Node(Characteristic):
    def __init__(self, name: str, parent, weights: List[int | float]):
        self.name = name
        self.parent = parent
        self.children = []
        self.weights = weights

    def measure(self):
        measurement = None
        for c in self.children:
            measurement += c.measure()

    def to_string(self):
        string = self.name + "\n"
        for child in self.children:
            string += child["ptr"].to_string()
        return string

    def __eq__(self, __o: object) -> bool:
        if __o.name != self.name:
            return False
        elif __o.children != self.children:
            return False
        elif __o.weights != self.weights:
            return False
        return True


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
