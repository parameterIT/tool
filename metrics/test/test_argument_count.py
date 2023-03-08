from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.argument_count import ArgumentCount


class TestArgumentCount(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_argument_count"), "python"
        )
        self._argumentcount = ArgumentCount()
        self._argumentcount.set_coordinator(self._coordinator)

    def test_argument_count_given_directory_returns_2(self):
        result = self._argumentcount.run()
        self.assertEqual(result, 2)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
