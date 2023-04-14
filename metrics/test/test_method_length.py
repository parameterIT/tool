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
        self._source_repository = SourceRepository(Path("./metrics/test/data/test_data_method_length"))
        self._methodlength = MethodLength()
        self._methodlength._source_repository = self._source_repository

    def test_method_length_given_python_file_returns_2(self):
        result = self._methodlength.run()
        self.assertEqual(result.outcome, 2)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (39, 73))
        self.assertEqual((locations[1][1], locations[1][2]), (76, 108))

    def test_method_length_given_java_file_returns_1(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_data_method_length"))
        method_length = MethodLength()
        method_length._source_repository = new_source_repository
        result = method_length.run()
        self.assertEqual(result.outcome, 1)

    def test_method_length_given_c_sharp_file_returns_3(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_data_method_length"))
        method_length = MethodLength()
        method_length._source_repository = new_source_repository
        result = method_length.run()
        self.assertEqual(result.outcome, 3)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
