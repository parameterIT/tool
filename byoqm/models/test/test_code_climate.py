from pathlib import Path
import unittest

from byoqm.models.code_climate import CodeClimate


class TestStringMethods(unittest.TestCase):
    def test_file_length_given_this_directory_returns_0(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 1
        actual = qm.file_length()

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
