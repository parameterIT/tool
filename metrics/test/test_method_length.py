from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.method_length import MethodLength


class TestMethodLength(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_method_length"), "python"
        )
        self._methodlength = MethodLength()
        self._methodlength.coordinator = self._coordinator

    def test_method_length_given_python_file_returns_2(self):
        result = self._methodlength.run()
        self.assertEqual(result, 2)

    def test_method_length_given_java_file_returns_1(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_method_length"), "java"
        )
        new_method_counter = MethodLength()
        new_method_counter.coordinator = new_coordinator
        result = new_method_counter.run()
        self.assertEqual(result,1)

    def test_method_length_given_c_sharp_file_returns_3(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_method_length"), "c_sharp"
        )
        new_method_counter = MethodLength()
        new_method_counter.coordinator = new_coordinator
        result = new_method_counter.run()
        self.assertEqual(result,3)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
