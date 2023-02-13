from ast import List
from byoqm.metric.metric import Metric
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
        return measurement


class TreeQualityModel(QualityModel):
    def __init__(self):
        self.root = Node("quality", None, [])

    def insert(self, parent, child):
        if self.find(child.name) != None:
            #TODO: Research traceback when raising a custom exception
            raise Exception('Node already exists in the quality model')

        self.find(parent).children.append(child)

    def keys(self):
        print(self._keys(self.root, ""))

    def _keys(self, node: Node, metrics: str):
        for n in node.children:
            if isinstance(n, Metric):
                metrics += " " + n.name
            else:
                self._keys(n, metrics)

    def find(self, name: str):
        for n in self.root.children:
            n._find(n, name)

    def _find(self, node: Node, name: str):
        if node.name == name:
            return node
        else:
            for n in node.children:
                n._find(n, name)

        #Should only be hit if no node with the given name is found
        return None

    def measure(self):
        self.root.measure()
