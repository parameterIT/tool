from pathlib import Path
import unittest
import os
from core.source_repository.source_repository import SourceRepository
from metrics.nested_controlflows import NestedControlflows


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_nested_controlflows")
        )
        self._nested_flow = NestedControlflows()
        self._nested_flow._source_repository = self._source_repository

    @unittest.expectedFailure
    def test_nested_controlflow_given_test_directory_returns_10(self):
        result = self._nested_flow.run()
        self.assertEqual(len(result), 10)

    def test_nested_controlflow_given_test_directory_returns_3(self):
        result = self._nested_flow.run()
        self.assertEqual(result.outcome, 3)

        locations = result.get_violation_locations()
        expected_locations = [
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py",
                3,
                19,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py",
                20,
                32,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py",
                51,
                59,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
