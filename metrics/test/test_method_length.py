from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.method_length import MethodLength


class TestMethodLength(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_length")
        )
        self._methodlength = MethodLength()
        self._methodlength._source_repository = self._source_repository

    def test_method_length_returns_6(self):
        result = self._methodlength.run()
        self.assertEqual(result.outcome, 6)

        locations = result.get_violation_locations()

        self.assertEqual((locations[3][1], locations[3][2]), (39, 73))
        self.assertEqual((locations[4][1], locations[4][2]), (76, 108))

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
