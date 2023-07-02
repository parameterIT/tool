from pathlib import Path
import unittest
from core.source_repository.source_repository import SourceRepository
from core.metric.violation import Location
from metrics.method_count import MethodCount


class TestMethodCount(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_count")
        )
        self._methodcount = MethodCount()
        self._methodcount._source_repository = self._source_repository

    def test_method_count_returns_3(self):
        result = self._methodcount.run()
        self.assertEqual(result.outcome, 3)
        locations = result.get_violation_locations()
        expected_locations = [
            Location(
                Path("metrics/test/data/test_data_method_count/data_method_count_1.cs"),
                3,
                98,
            ),
            Location(
                Path("metrics/test/data/test_data_method_count/data_method_count.java"),
                2,
                65,
            ),
            Location(
                Path("metrics/test/data/test_data_method_count/data_method_count.py"),
                1,
                81,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)


if __name__ == "__main__":
    unittest.main()
