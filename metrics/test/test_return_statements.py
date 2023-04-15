from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.return_statements import ReturnStatements


class TestReturnStatements(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_return_statements")
        )
        self._returnstmnt = ReturnStatements()
        self._returnstmnt._source_repository = self._source_repository

    def test_return_statements_returns_6(self):
        result = self._returnstmnt.run()
        self.assertEqual(result.outcome, 6)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (5, 15))
        self.assertEqual((locations[1][1], locations[1][2]), (18, 35))

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
