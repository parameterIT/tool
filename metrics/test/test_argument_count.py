from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.argument_count import ArgumentCount


class TestArgumentCount(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_argument_count"), "python"
        )
        self._argumentcount = ArgumentCount()
        self._argumentcount.coordinator = self._coordinator

    def test_argument_count_python_given_directory_returns_2(self):
        result = self._argumentcount.run()
        self.assertEqual(result, 2)
    def test_argument_count_c_sharp_given_directory_returns_2(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_argument_count"), "c_sharp"
        )
        argumentCount = ArgumentCount()
        argumentCount.coordinator = new_coordinator
        result = argumentCount.run()
        
        self.assertEqual(result, 2)
        
    def test_argument_count_java_given_directory_returns_2(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_argument_count"), "java"
        )
        argumentCount = ArgumentCount()
        argumentCount.coordinator = new_coordinator
        result = argumentCount.run()
        
        self.assertEqual(result, 2)
        
    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
