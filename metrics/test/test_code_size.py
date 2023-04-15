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
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_file_length")
        )
        self._code_size = CodeSize()
        self._code_size._source_repository = self._source_repository

    def test_code_size__files_returns_1768(self):
        result = self._code_size.run()
        self.assertEqual(result, 1768)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
