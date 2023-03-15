from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.return_statements import ReturnStatements


class TestReturnStatements(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_return_statements"), "python"
        )
        self._returnstmnt = ReturnStatements()
        self._returnstmnt.coordinator = self._coordinator

    def test_return_statements_given_python_fil_returns_2(self):
        result = self._returnstmnt.run()[0]
        self.assertEqual(result, 2)

    def test_argument_count_c_sharp_given_directory_returns_2(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_return_statements"), "c_sharp"
        )
        return_statements = ReturnStatements()
        return_statements.coordinator = new_coordinator
        result = return_statements.run()[0]
        self.assertEqual(result, 2)

    def test_argument_count_java_given_directory_returns_2(self):
        new_coordinator = SourceCoordinator(
            Path("./metrics/test/data/test_data_return_statements"), "java"
        )
        return_statements = ReturnStatements()
        return_statements.coordinator = new_coordinator
        result = return_statements.run()[0]
        self.assertEqual(result, 2)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
