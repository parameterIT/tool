from pathlib import Path
import unittest
from core.source_repository.source_repository import SourceRepository
from core.metric.violation import Location
from metrics.return_statements import ReturnStatements


class TestReturnStatements(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_return_statements")
        )
        self._return_stmnt = ReturnStatements()
        self._return_stmnt._source_repository = self._source_repository

    def test_return_statements_returns_6(self):
        result = self._return_stmnt.run()
        self.assertEqual(result.outcome, 6)
        locations = result.get_violation_locations()
        expected_locations = [
            Location(
                Path(
                    "metrics/test/data/test_data_return_statements/data_return_statements.py"
                ),
                5,
                15,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_return_statements/data_return_statements.py"
                ),
                18,
                35,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_return_statements/data_return_statements.cs"
                ),
                5,
                13,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_return_statements/data_return_statements.cs"
                ),
                21,
                28,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_return_statements/data_return_statements.java"
                ),
                5,
                24,
            ),
            Location(
                Path(
                    "metrics/test/data/test_data_return_statements/data_return_statements.java"
                ),
                41,
                57,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)


if __name__ == "__main__":
    unittest.main()
