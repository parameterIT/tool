from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.method_count import MethodCount


class TestMethodCount(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_method_count"), "python"
        )
        self._methodcount = MethodCount()
        self._methodcount.coordinator = self._coordinator

    def test_method_count_given_file_returns_1(self):
        result = self._methodcount.run()
        self.assertEqual(result, 1)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
