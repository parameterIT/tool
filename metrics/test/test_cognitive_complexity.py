import unittest

from pathlib import Path
from core.metric.metric import Metric

from core.source_repository.source_repository import SourceRepository
from metrics.cognitive_complexity import CognitiveComplexity


class TestCognitiveComplexity(unittest.TestCase):
    def setUp(self):
        self._source_repository: SourceRepository = SourceRepository(
            Path("./metrics/test/data/test_cognitive_complexity/test_recursion")
        )
        self._metric: Metric = CognitiveComplexity()
        self._metric._source_repository = self._source_repository

    def test_recursion_returns_3(self):
        result = self._metric.run()
        actual = result.outcome
        expected = 3
        self.assertEqual(actual, expected)

        locations = result.get_violation_locations()
        expected_locations = [
            (
                "metrics/test/data/test_cognitive_complexity/test_recursion/data_recursion.py",
                1,
                8,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_recursion/data_recursion.java",
                5,
                13,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_recursion/data_recursion.cs",
                5,
                15,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)

    def test_breaks_in_linear_flow_returns_3(self):
        new_source_repository = SourceRepository(
            Path(
                "./metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow"
            )
        )
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 3
        self.assertEqual(actual, expected)

        locations = result.get_violation_locations()
        expected_locations = [
            (
                "metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow/data_breaks_in_linear_flow.cs",
                10,
                49,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow/data_breaks_in_linear_flow.py",
                1,
                25,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow/data_breaks_in_linear_flow.java",
                5,
                42,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)

    def test_cognitive_complexity_returns_18(self):
        new_source_repository = SourceRepository(
            Path(
                "./metrics/test/data/test_cognitive_complexity/test_nested_controlflows"
            )
        )
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 18
        self.assertEqual(actual, expected)

    def test_cognitive_complexity_returns_30(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_cognitive_complexity")
        )
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 30
        self.assertEqual(actual, expected)
