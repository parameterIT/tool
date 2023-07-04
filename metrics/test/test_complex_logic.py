from pathlib import Path
import unittest
from core.source_repository.source_repository import SourceRepository
from core.metric.violation import Location
from metrics.complex_logic import ComplexLogic


class TestComplexLogic(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_complex_logic")
        )
        self._complexlogic = ComplexLogic()
        self._complexlogic._source_repository = self._source_repository

    def test_complex_logic_given_file_returns_10(self):
        result = self._complexlogic.run()
        self.assertEqual(result.outcome, 10)

        locations = result.get_violation_locations()
        expected_locations = [
            Location(
                Path("metrics/test/data/test_data_complex_logic/data_complex_logc.cs"),
                11,
                11,
            ),
            Location(
                Path("metrics/test/data/test_data_complex_logic/data_complex_logc.cs"),
                12,
                12,
            ),
            Location(
                Path("metrics/test/data/test_data_complex_logic/data_complex_logc.cs"),
                15,
                15,
            ),
            Location(
                Path("metrics/test/data/test_data_complex_logic/data_complex_logc.cs"),
                17,
                17,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_complex_logic/data_complex_logic.java"
                ),
                15,
                15,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_complex_logic/data_complex_logic.java"
                ),
                16,
                16,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_complex_logic/data_complex_logic.java"
                ),
                19,
                19,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_complex_logic/data_complex_logic.java"
                ),
                21,
                21,
            ),
            Location(
                Path("metrics/test/data/test_data_complex_logic/data_complex_logic.py"),
                20,
                20,
            ),
            Location(
                Path("metrics/test/data/test_data_complex_logic/data_complex_logic.py"),
                23,
                23,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)


if __name__ == "__main__":
    unittest.main()
