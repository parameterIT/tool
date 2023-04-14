from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.code_size import CodeSize


class TestCodeSize(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(Path("./metrics/test/data/test_data_file_length"))
        self._code_size = CodeSize()
        self._code_size._source_repository = self._source_repository

    def test_code_size_given_python_files_returns_251(self):
        result = self._code_size.run()
        self.assertEqual(result, 251)

    def test_code_size_given_java_files_returns_501(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_data_file_length"))
        code_size = CodeSize()
        code_size._source_repository = new_source_repository
        result = code_size.run()
        self.assertEqual(result, 501)

    def test_code_size_given_csharp_files_returns_1016(self):
        new_source_repository = SourceRepository(Path("./metrics/test/data/test_data_file_length"))
        code_size = CodeSize()
        code_size._source_repository = new_source_repository
        result = code_size.run()
        self.assertEqual(result, 1016)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
