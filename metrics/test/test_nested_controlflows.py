from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.nested_controlflows import NestedControlflows


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_nested_controlflows"), "python"
        )
        self._nestedflow = NestedControlflows()
        self._nestedflow.coordinator = self._coordinator

    @unittest.expectedFailure
    def test_nested_controlflow_given_test_directory_returns_9(self):
        result = self._nestedflow.run()
        self.assertEqual(result, 9)

    def test_method_length_given_c_sharp_file_returns_3(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_nested_controlflows"), "c_sharp"
        )
        self.assertEqual(len(new_coordinator.src_paths), 1)
        nested_control_flow = NestedControlflows()
        nested_control_flow.coordinator = new_coordinator
        result = nested_control_flow.run()
        self.assertEqual(result, 3)

    def test_method_length_given_java_file_returns_5(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_nested_controlflows"), "java"
        )
        self.assertEqual(len(new_coordinator.src_paths), 1)
        nested_control_flow = NestedControlflows()
        nested_control_flow.coordinator = new_coordinator
        result = nested_control_flow.run()
        self.assertEqual(result, 5)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
