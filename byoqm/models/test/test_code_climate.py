from pathlib import Path
import unittest

from byoqm.models.code_climate import CodeClimate


class TestCodeClimate(unittest.TestCase):
    def test_file_length_given_this_directory_returns_1(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 1
        actual = qm.file_length()

        self.assertEqual(actual, expected)

    def test_method_count_given_this_directory_returns_1(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 1
        actual = qm.method_count()

        self.assertEqual(actual, expected)

    def test_argument_count_given_this_directory_returns_2(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 2
        actual = qm.argument_count()

        self.assertEqual(actual, expected)

    def test_return_statements_given_this_directory_returns_2(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 2
        actual = qm.return_statements()

        self.assertEqual(actual, expected)

    def test_method_length_given_this_repository_returns_2(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 2
        actual = qm.method_length()

        self.assertEqual(actual, expected)

    def test_identical_code_given_test_data_directoy_returns_3(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test/data2/"))

        expected = 4
        actual = qm.identical_blocks_of_code()
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
