import unittest
from pathlib import Path
from byoqm.metric.metric import Metric

from byoqm.qm_parser.yml_parser import YMLParser
from byoqm.qualitymodel.treequalitymodel import Node


class TestYMLParser(unittest.TestCase):
    parser = YMLParser()

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

    def test_parse_yml_test_file(self):
        path = Path("yml_test_file.yml")
        actual_quality = self.parser.parse(path)
        print(actual_quality.to_string())
        self.assertEqual(self.expected_quality, actual_quality)


if __name__ == "__main__":
    unittest.main()
