from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.return_statements import ReturnStatements


class TestReturnStatements(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_return_statements"), "python"
        )
        self._returnstmnt = ReturnStatements()
        self._returnstmnt.coordinator = self._coordinator

    def test_return_statements_given_file_returns_2(self):
        result = self._returnstmnt.run()
        self.assertEqual(result, 2)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
