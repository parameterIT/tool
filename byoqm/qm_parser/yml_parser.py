from typing import List
from qm_parser import Parser
from qualitymodel import QualityModel, Node
import yaml
from pathlib import Path


class YMLParser(Parser):
    # TODO: Finding metrics, failing if they don't exist
    # TODO: Parse weights
    def parse(self, file_path: Path) -> Node:
        stream = open(file_path, "r")
        dictionary = yaml.load(stream, Loader=yaml.FullLoader)
        root = self._parse("Quality", dictionary)
        return root

    def _parse(self, name: str, children, parent: Node = None) -> Node:
        # List of all keys = list of children names
        # For each children name generate a child node
        # Collect the child nodes in list
        node = Node(name, parent, [])

        children = []
        for k, v in children:
            if k == "Metric":
                children.append(self._parse_metrics(v))
            else:
                children.append(self._parse(k, v, node))
        node.children = children

        return node

    def _parse_metrics(self, metrics):
        for m in metrics:
            # search /metrics for the executable
            pass
        return []
