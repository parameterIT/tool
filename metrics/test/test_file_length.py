from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.file_length import FileLength


class TestFileLength(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_file_length"), "python"
        )
        self._filelength = FileLength()
        self._filelength.coordinator = self._coordinator

    def test_file_length_given_file_returns_1(self):
        result = self._filelength.run()
        self.assertEqual(result, 1)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
