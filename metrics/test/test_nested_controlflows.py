from pathlib import Path
import unittest
from core.source_repository.source_repository import SourceRepository
from core.metric.violation import Location
from metrics.nested_controlflows import NestedControlflows


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_nested_controlflows")
        )
        self._nested_flow = NestedControlflows()
        self._nested_flow._source_repository = self._source_repository

    def test_nested_controlflow_given_test_directory_returns_22(self):
        result = self._nested_flow.run()
        self.assertEqual(result.outcome, 22)

        locations = result.get_violation_locations()
        expected_locations = [
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_control_flow_switches.java"
                ),
                3,
                10,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_control_flow_switches.java"
                ),
                18,
                27,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_switches.cs"
                ),
                10,
                18,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_switches2.cs"
                ),
                2,
                13,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs"
                ),
                6,
                13,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs"
                ),
                23,
                34,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs"
                ),
                37,
                48,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows.cs"
                ),
                60,
                74,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_2.py"
                ),
                1,
                6,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_2.py"
                ),
                8,
                13,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py"
                ),
                3,
                19,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py"
                ),
                20,
                32,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py"
                ),
                45,
                49,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_3.py"
                ),
                51,
                59,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_1.py"
                ),
                4,
                8,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_1.py"
                ),
                10,
                14,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java"
                ),
                7,
                14,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java"
                ),
                15,
                24,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java"
                ),
                32,
                39,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java"
                ),
                41,
                48,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_control_flows.java"
                ),
                50,
                61,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_nested_controlflows/data_nested_controlflows_5.py"
                ),
                3,
                10,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)


if __name__ == "__main__":
    unittest.main()
