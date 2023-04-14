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

    def test_recursion_given_python_recursion_file_returns_1(self):
        result = self._metric.run()
        actual = result.outcome
        expected = 1
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (1, 8))

    def test_recursion_given_c_sharp_recursion_file_returns_1(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_cognitive_complexity/test_recursion"))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 1
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (5, 15))

    def test_recursion_given_java_recursion_file_returns_1(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_cognitive_complexity/test_recursion"))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 1
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (5, 13))

    def test_breaks_in_linear_flow_given_python_file_returns_1(self):
        new_source_repository = SourceRepository(Path(
            "./metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow"
        ))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 1
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (1, 25))

    def test_breaks_in_linear_flow_given_c_sharp_file_returns_1(self):
        new_source_repository = SourceRepository(Path(
            "./metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow"
        ))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 1
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (10, 49))

    def test_breaks_in_linear_flow_given_java_file_returns_1(self):
        new_source_repository = SourceRepository(Path(
            "./metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow"
        ))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 1
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (5, 42))

    def test_cognitive_complexity_for_python_returns_4(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_cognitive_complexity"))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 4
        self.assertEqual(actual, expected)

    def test_cognitive_complexity_for_c_sharp_returns_4(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_cognitive_complexity"))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 4
        self.assertEqual(actual, expected)

    def test_cognitive_complexity_for_java_returns_4(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_cognitive_complexity"))
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 4
        self.assertEqual(actual, expected)
