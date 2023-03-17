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
            Path("./metrics/test/data/test_data_method_length"), "python"
        )
        self._methodlength = MethodLength()
        self._methodlength._source_repository = self._source_repository

    def test_method_length_given_python_file_returns_2(self):
        result = len(self._methodlength.run())
        self.assertEqual(result, 2)

    def test_method_length_given_java_file_returns_1(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_length"), "java"
        )
        method_length = MethodLength()
        method_length._source_repository = new_source_repository
        result = len(method_length.run())
        self.assertEqual(result, 1)

    def test_method_length_given_c_sharp_file_returns_3(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_length"), "c_sharp"
        )
        method_length = MethodLength()
        method_length._source_repository = new_source_repository
        result = len(method_length.run())
        self.assertEqual(result, 3)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
