from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.nested_controlflows import NestedControlflows


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_nested_controlflows"), "python"
        )
        self._nestedflow = NestedControlflows()
        self._nestedflow.set_coordinator(self._coordinator)

    @unittest.expectedFailure
    def test_nested_controlflow_given_test_directory_returns_9(self):
        result = self._nestedflow.run()
        self.assertEqual(result, 9)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
