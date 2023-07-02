from pathlib import Path
import unittest
from core.source_repository.source_repository import SourceRepository
from core.metric.violation import Location
from metrics.argument_count import ArgumentCount


class TestArgumentCount(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_argument_count")
        )
        self._argumentcount = ArgumentCount()
        self._argumentcount._source_repository = self._source_repository

    def test_argument_count_given_directory_returns_6(self):
        result = self._argumentcount.run()
        self.assertEqual(result.outcome, 6)

        locations = result.get_violation_locations()
        expected_locations = [
            Location(
                Path("metrics/test/data/test_data_argument_count/data_argument_count.cs"),
                9, 9
            ),
            Location(
                Path("metrics/test/data/test_data_argument_count/data_argument_count.cs"),
                10, 10
            ),
            Location(
                Path("metrics/test/data/test_data_argument_count/data_argument_count.py"),
                13, 13
            ),
            Location(
                Path("metrics/test/data/test_data_argument_count/data_argument_count.py"),
                18, 18
            ),
            Location(
                Path("metrics/test/data/test_data_argument_count/data_argument_count.java"),
                17, 17
            ),
            Location(
                Path("metrics/test/data/test_data_argument_count/data_argument_count.java"),
                20, 20
            ),
        ]
        self.assertCountEqual(locations, expected_locations)


if __name__ == "__main__":
    unittest.main()
