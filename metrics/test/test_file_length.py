from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.file_length import FileLength


class TestFileLength(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_file_length"), "python"
        )
        self._filelength = FileLength()
        self._filelength.coordinator = self._coordinator

    def test_file_length_given_python_file_returns_1(self):
        result = self._filelength.run()[0]
        self.assertEqual(result, 1)

    def test_file_length_given_java_file_returns_1(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_file_length"), "java"
        )
        new_method_counter = FileLength()
        new_method_counter.coordinator = new_coordinator
        result = new_method_counter.run()[0]
        self.assertEqual(result, 1)

    def test_file_length_given_csharp_file_returns_1(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_file_length"), "c_sharp"
        )
        new_method_counter = FileLength()
        new_method_counter.coordinator = new_coordinator
        result = new_method_counter.run()[0]
        self.assertEqual(result, 1)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
