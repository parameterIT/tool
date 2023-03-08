from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.method_length import MethodLength


class TestMethodLength(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_method_length"), "python"
        )
        self._methodlength = MethodLength()
        self._methodlength.set_coordinator(self._coordinator)

    def test_method_length_given_file_returns_2(self):
        result = self._methodlength.run()
        self.assertEqual(result, 2)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
