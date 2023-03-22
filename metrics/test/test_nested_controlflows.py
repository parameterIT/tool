from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.nested_controlflows import NestedControlflows


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_nested_controlflows"), "python"
        )
        self._nestedflow = NestedControlflows()
        self._nestedflow._source_repository = self._source_repository

    @unittest.expectedFailure
    def test_nested_controlflow_given_test_directory_returns_10(self):
        result = self._nestedflow.run()
        self.assertEqual(len(result), 10)

    def test_nested_controlflow_given_test_directory_returns_9(self):
        result = self._nestedflow.run()
        locations = result.get_violation_locations()
        self.assertEqual(result.get_frequency(), 9)
        self.assertEqual((locations[0][1], locations[0][2]), (3, 10))
        self.assertEqual((locations[1][1], locations[1][2]), (4, 8))
        self.assertEqual((locations[2][1], locations[2][2]), (10, 14))
        self.assertEqual((locations[3][1], locations[3][2]), (1, 6))
        self.assertEqual((locations[4][1], locations[4][2]), (8, 13))
        self.assertEqual((locations[5][1], locations[5][2]), (3, 19))
        self.assertEqual((locations[6][1], locations[6][2]), (20, 32))
        self.assertEqual((locations[7][1], locations[7][2]), (45, 49))
        self.assertEqual((locations[8][1], locations[8][2]), (51, 59))

    def test_nested_control_flow_given_c_sharp_file_returns_6(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_nested_controlflows"), "c_sharp"
        )
        self.assertEqual(len(new_source_repository.src_paths), 3)
        nested_control_flow = NestedControlflows()
        nested_control_flow._source_repository = new_source_repository
        result = nested_control_flow.run()
        self.assertEqual(result.get_frequency(), 6)

    def test_nested_control_flow_given_java_file_returns_7(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_nested_controlflows"), "java"
        )
        self.assertEqual(len(new_source_repository.src_paths), 2)
        nested_control_flow = NestedControlflows()
        nested_control_flow._source_repository = new_source_repository
        result = nested_control_flow.run()
        self.assertEqual(result.get_frequency(), 7)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
