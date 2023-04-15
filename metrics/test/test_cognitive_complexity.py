import os
import unittest

from pathlib import Path
from byoqm.metric.metric import Metric

from byoqm.source_repository.source_repository import SourceRepository
from metrics.cognitive_complexity import CognitiveComplexity


class TestCognitiveComplexity(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository: SourceRepository = SourceRepository(
            Path("./metrics/test/data/test_cognitive_complexity/test_recursion"))
        self._metric: Metric = CognitiveComplexity()
        self._metric._source_repository = self._source_repository

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())

    def test_recursion_returns_3(self):
        result = self._metric.run()
        actual = result.outcome
        expected = 3
        self.assertEqual(actual, expected)

        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (1, 8))
        self.assertEqual((locations[1][1], locations[1][2]), (5, 13))
        self.assertEqual((locations[2][1], locations[2][2]), (5, 15))

    def test_breaks_in_linear_flow_returns_3(self):
        new_source_repository = SourceRepository(Path(
            "./metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow"
        ))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 3
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (10, 49))
        self.assertEqual((locations[1][1], locations[1][2]), (1, 25))
        self.assertEqual((locations[2][1], locations[2][2]), (5, 42))

    def test_cognitive_complexity_returns_12(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_cognitive_complexity"))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 12
        self.assertEqual(actual, expected)
