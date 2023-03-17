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
        result = self._complexlogic.run()
        self.assertEqual(len(result), 2)
        self.assertEqual((result[0][2], result[0][3]), ("20", "20"))
        self.assertEqual((result[1][2], result[1][3]), ("23", "23"))

    def test_argument_count_c_sharp_given_directory_returns_4(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_complex_logic"), "c_sharp"
        )
        complex_logic = ComplexLogic()
        complex_logic._source_repository = new_source_repository
        result = complex_logic.run()

        self.assertEqual(len(result), 4)
        self.assertEqual((result[0][2], result[0][3]), ("11", "11"))
        self.assertEqual((result[1][2], result[1][3]), ("12", "12"))
        self.assertEqual((result[2][2], result[2][3]), ("15", "15"))
        self.assertEqual((result[3][2], result[3][3]), ("17", "17"))

    def test_argument_java_sharp_given_directory_returns_4(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_complex_logic"), "java"
        )
        complex_logic = ComplexLogic()
        complex_logic._source_repository = new_source_repository
        result = complex_logic.run()

        self.assertEqual(len(result), 4)
        self.assertEqual((result[0][2], result[0][3]), ("15", "15"))
        self.assertEqual((result[1][2], result[1][3]), ("16", "16"))
        self.assertEqual((result[2][2], result[2][3]), ("19", "19"))
        self.assertEqual((result[3][2], result[3][3]), ("21", "21"))

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
