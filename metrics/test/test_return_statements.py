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
        result = self._returnstmnt.run()
        self.assertEqual(len(result), 2)
        self.assertEqual((result[0][2],result[0][3]),('5','15'))
        self.assertEqual((result[1][2],result[1][3]),('18','35'))

    def test_argument_count_c_sharp_given_directory_returns_2(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_return_statements"), "c_sharp"
        )
        return_statements = ReturnStatements()
        return_statements._source_repository = new_source_repository
        result = return_statements.run()
        self.assertEqual(len(result), 2)

    def test_argument_count_java_given_directory_returns_2(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_return_statements"), "java"
        )
        return_statements = ReturnStatements()
        return_statements._source_repository = new_source_repository
        result = return_statements.run()
        self.assertEqual(len(result), 2)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
