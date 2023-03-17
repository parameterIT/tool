from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.argument_count import ArgumentCount


class TestArgumentCount(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_argument_count"), "python"
        )
        self._argumentcount = ArgumentCount()
        self._argumentcount._source_repository = self._source_repository

    def test_argument_count_python_given_directory_returns_2(self):
        result = len(self._argumentcount.run())
        self.assertEqual(result, 2)

    def test_argument_count_c_sharp_given_directory_returns_2(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_argument_count"), "c_sharp"
        )
        argument_count = ArgumentCount()
        argument_count._source_repository = new_source_repository
        result = len(argument_count.run())

        self.assertEqual(result, 2)

    def test_argument_count_java_given_directory_returns_2(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_argument_count"), "java"
        )
        argument_count = ArgumentCount()
        argument_count._source_repository = new_source_repository
        result = len(argument_count.run())

        self.assertEqual(result, 2)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
