from pathlib import Path
import unittest
import os
from core.source_repository.source_repository import SourceRepository
from metrics.nested_controlflows import NestedControlflows


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_nested_controlflows")
        )
        self._nested_flow = NestedControlflows()
        self._nested_flow._source_repository = self._source_repository

    @unittest.expectedFailure
    def test_nested_controlflow_given_test_directory_returns_10(self):
        result = self._nested_flow.run()
        self.assertEqual(len(result), 10)

    def test_nested_controlflow_given_test_directory_returns_22(self):
        result = self._nested_flow.run()
        self.assertEqual(result.outcome, 22)

        locations = result.get_violation_locations()
        expected_locations = [
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_control_flow_switches.java",
                3,
                10,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_control_flow_switches.java",
                18,
                27,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_switches.cs",
                10,
                18,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_switches2.cs",
                2,
                13,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs",
                6,
                13,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs",
                23,
                34,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs",
                37,
                48,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs",
                60,
                74,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_2.py",
                1,
                6,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_2.py",
                8,
                13,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py",
                3,
                19,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py",
                20,
                32,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py",
                45,
                49,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py",
                51,
                59,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_1.py",
                4,
                8,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_1.py",
                10,
                14,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java",
                7,
                14,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java",
                15,
                24,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java",
                32,
                39,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java",
                41,
                48,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java",
                50,
                61,
            ),
            (
                "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_5.py",
                3,
                10,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
