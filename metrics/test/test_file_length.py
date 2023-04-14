from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.file_length import FileLength


class TestFileLength(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(Path("./metrics/test/data/test_data_file_length"))
        self._filelength = FileLength()
        self._filelength._source_repository = self._source_repository

    def test_file_length_given_python_file_returns_1(self):
        result = self._filelength.run()
        self.assertEqual(result.outcome, 1)

    def test_file_length_given_java_file_returns_1(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_data_file_length"))
        file_length = FileLength()
        file_length._source_repository = new_source_repository
        result = file_length.run()
        self.assertEqual(result.outcome, 1)

    def test_file_length_given_csharp_file_returns_3(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_data_file_length"))
        file_length = FileLength()
        file_length._source_repository = new_source_repository
        result = file_length.run()
        self.assertEqual(result.outcome, 3)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
