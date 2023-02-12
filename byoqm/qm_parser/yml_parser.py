from typing import Dict
from byoqm.metric.metric import Metric
from byoqm.qm_parser.parser import Parser
from byoqm.qualitymodel import Node
import yaml
from pathlib import Path


class YMLParser(Parser):
    def parse(self, file_path: Path) -> Node:
        stream = open(file_path, "r")
        dictionary = yaml.load(stream, Loader=yaml.FullLoader)
        root = self._parse("Quality", None, dictionary)
        return root

    def _parse(self, name: str, parent: Node, characteristics: Dict) -> Node:
        characteristic = Node(name, parent, [])
        for subcharacteristic in characteristics:
            child = {"weight": 1, "ptr": None}
            if subcharacteristic == "weight":
                # The current weight is relevant to the parent and has already been
                # read, so it is skipped
                pass
            elif subcharacteristic == "Metrics":
                for m in characteristics[subcharacteristic]:
                    # TODO: Find actual executables, failing if they do not exist
                    for key in m:
                        if key == "weight":
                            child["weight"] = m["weight"]
                        else:
                            child["ptr"] = Metric(Path(key))
                    characteristic.children.append(child.copy())
            else:
                child["weight"] = characteristics[subcharacteristic]["weight"]
                child["ptr"] = self._parse(
                    subcharacteristic,
                    characteristic,
                    characteristics[subcharacteristic],
                )
                characteristic.children.append(child.copy())

        return characteristic
