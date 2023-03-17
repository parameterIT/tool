from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.complex_logic import ComplexLogic


class TestComplexLogic(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_complex_logic"), "python"
        )
        self._complexlogic = ComplexLogic()
        self._complexlogic._source_repository = self._source_repository

    def test_complex_logic_given_file_returns_2(self):
        result = len(self._complexlogic.run())
        self.assertEqual(result, 2)

    def test_argument_count_c_sharp_given_directory_returns_4(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_complex_logic"), "c_sharp"
        )
        complex_logic = ComplexLogic()
        complex_logic._source_repository = new_source_repository
        result = len(complex_logic.run())

        self.assertEqual(result, 4)

    def test_argument_java_sharp_given_directory_returns_4(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_complex_logic"), "java"
        )
        complex_logic = ComplexLogic()
        complex_logic._source_repository = new_source_repository
        result = len(complex_logic.run())

        self.assertEqual(result, 4)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
