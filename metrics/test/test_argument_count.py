from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.argument_count import ArgumentCount


class TestArgumentCount(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_argument_count")
        )
        self._argumentcount = ArgumentCount()
        self._argumentcount._source_repository = self._source_repository

    def test_argument_count_given_directory_returns_6(self):
        result = self._argumentcount.run()
        self.assertEqual(result.outcome, 6)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (9, 9))
        self.assertEqual((locations[1][1], locations[1][2]), (10, 10))
        self.assertEqual((locations[2][1], locations[2][2]), (13, 13))
        self.assertEqual((locations[3][1], locations[3][2]), (18, 18))
        self.assertEqual((locations[4][1], locations[4][2]), (17, 17))
        self.assertEqual((locations[5][1], locations[5][2]), (20, 20))

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
