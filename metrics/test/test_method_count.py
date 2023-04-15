from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.method_count import MethodCount


class TestMethodCount(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(Path("./metrics/test/data/test_data_method_count"))
        self._methodcount = MethodCount()
        self._methodcount._source_repository = self._source_repository

    def test_method_count_returns_3(self):
        result = self._methodcount.run()
        self.assertEqual(result.outcome, 3)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (1, 81))

        self.assertEqual((locations[0][1], locations[0][2]), (2, 65))

        self.assertEqual((locations[0][1], locations[0][2]), (3, 98))


    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
