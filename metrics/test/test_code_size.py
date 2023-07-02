from pathlib import Path
import unittest
from core.source_repository.source_repository import SourceRepository
from metrics.code_size import CodeSize


class TestCodeSize(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_file_length")
        )
        self._code_size = CodeSize()
        self._code_size._source_repository = self._source_repository

    def test_code_size__files_returns_1768(self):
        result = self._code_size.run()
        self.assertEqual(result, 1768)


if __name__ == "__main__":
    unittest.main()
