from pathlib import Path
import unittest
import os
from core.source_repository.source_repository import SourceRepository
from metrics.method_count import MethodCount


class TestMethodCount(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_count")
        )
        self._methodcount = MethodCount()
        self._methodcount._source_repository = self._source_repository

    def test_method_count_returns_3(self):
        result = self._methodcount.run()
        self.assertEqual(result.outcome, 3)
        locations = result.get_violation_locations()
        expected_locations = [
            ("metrics/test/data/test_data_method_count/data_method_count_1.cs", 3, 98),
            ("metrics/test/data/test_data_method_count/data_method_count.java", 2, 65),
            ("metrics/test/data/test_data_method_count/data_method_count.py", 1, 81),
        ]
        self.assertCountEqual(locations, expected_locations)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
