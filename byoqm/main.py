from pathlib import Path
from byoqm import qualitymodel
from metric import Metric
from qualitymodel.treequalitymodel import Node
from qm_parser import YMLParser

parser = YMLParser()
path = Path("yml_test_file.yml")
root = parser.parse(path.resolve())

expected_quality = Node("Quality", None, [])

expected_maintainability = Node("Maintainability", expected_quality, [])

expected_readability = Node("Readability", expected_maintainability, [])
expected_loc = Metric(Path("LOC"))

expected_complexiety = Node("Complexiety", expected_maintainability, [])
expected_duplication = Metric(Path("Duplication"))
expected_cyclomatic = Metric(Path("Cyclomatic"))

expected_reliability = Node("Reliability", expected_quality, [])
expected_code_coverage = Metric(Path("CodeCoverage"))

expected_quality.children = [
    {"weight": 2, "ptr": expected_maintainability},
    {"weight": 2, "ptr": expected_reliability},
]
expected_maintainability.children = [
    {"weight": 4, "ptr": expected_readability},
    {"weight": 5, "ptr": expected_complexiety},
]
expected_reliability.children = [{"weight": 2, "ptr": expected_code_coverage}]

expected_readability.children = [{"weight": 23, "ptr": expected_loc}]
expected_complexiety.children = [
    {"weight": 4, "ptr": expected_duplication},
    {"weight": 5, "ptr": expected_cyclomatic},
]

print(f"parsed: {root.to_string()}")
print(f"expected: {expected_quality.to_string()}")
