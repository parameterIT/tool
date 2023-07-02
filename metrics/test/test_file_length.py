from pathlib import Path
import unittest
import os
from core.source_repository.source_repository import SourceRepository
from metrics.file_length import FileLength


class TestFileLength(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_file_length")
        )
        self._filelength = FileLength()
        self._filelength._source_repository = self._source_repository

    def test_file_length_returns_5(self):
        result = self._filelength.run()
        self.assertEqual(result.outcome, 5)


if __name__ == "__main__":
    unittest.main()
