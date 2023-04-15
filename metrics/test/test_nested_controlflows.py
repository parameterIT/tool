from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.nested_controlflows import NestedControlflows


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_nested_controlflows")
        )
        self._nestedflow = NestedControlflows()
        self._nestedflow._source_repository = self._source_repository

    @unittest.expectedFailure
    def test_nested_controlflow_given_test_directory_returns_10(self):
        result = self._nestedflow.run()
        self.assertEqual(len(result), 10)

    def test_nested_controlflow_given_test_directory_returns_22(self):
        result = self._nestedflow.run()
        self.assertEqual(result.outcome, 22)
        reported_lines = set()
        for location in result.get_violation_locations():
            reported_lines.add((location[1], location[2]))
        self.assertIn((3, 10), reported_lines)
        self.assertIn((4, 8), reported_lines)
        self.assertIn((10, 14), reported_lines)
        self.assertIn((1, 6), reported_lines)
        self.assertIn((8, 13), reported_lines)
        self.assertIn((3, 19), reported_lines)
        self.assertIn((20, 32), reported_lines)
        self.assertIn((45, 49), reported_lines)
        self.assertIn((51, 59), reported_lines)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
