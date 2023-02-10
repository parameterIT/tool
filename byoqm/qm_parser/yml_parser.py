from typing import List
from qm_parser import Parser
from qualitymodel import QualityModel
import yaml


class YMLParser(Parser):
    
    def parse_children(self, children: dict, parent : Node = None) -> List[Node]:
        nodes = []
        for key, value in children.items():
            if key != "Metrics":
                nodes.append(Node(key, parent, self.parse_children(value)))
            else:
                for metric, value in value.items():
                    nodes.append(Node(metric, parent, value))
        return nodes
    
    def parse(self, file_path: str) -> QualityModel:
        #quality_md = QualityModel()
        stream = open(file_path, 'r')
        dictionary = yaml.load(stream, Loader=yaml.FullLoader)
        nodes = self.parse_children(dictionary)
        for node in nodes:
            #quality_md.insert(node)
        
    
        