from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.complex_logic import ComplexLogic


class TestComplexLogic(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(Path("./metrics/test/data/test_data_complex_logic"))
        self._complexlogic = ComplexLogic()
        self._complexlogic._source_repository = self._source_repository

    def test_complex_logic_given_file_returns_10(self):
        result = self._complexlogic.run()
        self.assertEqual(result.outcome, 10)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (20, 20))
        self.assertEqual((locations[1][1], locations[1][2]), (23, 23))

        self.assertEqual((locations[0][1], locations[0][2]), (11, 11))
        self.assertEqual((locations[1][1], locations[1][2]), (12, 12))
        self.assertEqual((locations[2][1], locations[2][2]), (15, 15))
        self.assertEqual((locations[3][1], locations[3][2]), (17, 17))

        self.assertEqual((locations[0][1], locations[0][2]), (15, 15))
        self.assertEqual((locations[1][1], locations[1][2]), (16, 16))
        self.assertEqual((locations[2][1], locations[2][2]), (19, 19))
        self.assertEqual((locations[3][1], locations[3][2]), (21, 21))

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
