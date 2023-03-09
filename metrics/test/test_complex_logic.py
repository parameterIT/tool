from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.complex_logic import ComplexLogic


class TestComplexLogic(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_complex_logic"), "python"
        )
        self._complexlogic = ComplexLogic()
        self._complexlogic.coordinator = self._coordinator

    def test_complex_logic_given_file_returns_4(self):
        result = self._complexlogic.run()
        self.assertEqual(result, 4)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
