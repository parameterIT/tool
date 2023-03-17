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
            Path("./metrics/test/data/test_data_return_statements"), "python"
        )
        self._returnstmnt = ReturnStatements()
        self._returnstmnt._source_repository = self._source_repository

    def test_return_statements_given_python_fil_returns_2(self):
        result = len(self._returnstmnt.run())
        self.assertEqual(result, 2)

    def test_argument_count_c_sharp_given_directory_returns_2(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_return_statements"), "c_sharp"
        )
        return_statements = ReturnStatements()
        return_statements._source_repository = new_source_repository
        result = len(return_statements.run())
        self.assertEqual(result, 2)

    def test_argument_count_java_given_directory_returns_2(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_return_statements"), "java"
        )
        return_statements = ReturnStatements()
        return_statements._source_repository = new_source_repository
        result = len(return_statements.run())
        self.assertEqual(result, 2)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
