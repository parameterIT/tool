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

    def test_nested_control_flow_given_ifstmts_returns_2(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test/data/if_stmts.py"))

        expected = 2
        actual = qm.nested_control_flow()

        self.assertEqual(actual, expected)

    def test_nested_control_flow_given_for_loops_returns_2(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test/data/for_loops.py"))

        expected = 2
        actual = qm.nested_control_flow()

        self.assertEqual(actual, expected)

    def test_nested_control_flow_given_while_loops_returns_1(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test/data/while_loops.py"))

        expected = 1
        actual = qm.nested_control_flow()

        self.assertEqual(actual, expected)

    def test_nested_control_flow_given_match_statements_returns_1(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test/data/match_statements.py"))

        expected = 1
        actual = qm.nested_control_flow()

        self.assertEqual(actual, expected)

    @unittest.expectedFailure
    def test_nested_control_flow_given_if_elif_else_statements_returns_4(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test/data/if_elif_else_statements.py"))

        expected = 4
        actual = qm.nested_control_flow()

        self.assertEqual(actual, expected)

    def test_method_length_given_this_repository_returns_2(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 2
        actual = qm.method_length()

        self.assertEqual(actual, expected)

    def test_complex_logic_given_this_repository_returns_3(self):
        qm = CodeClimate()
        qm.set_src_root(Path("byoqm/models/test"))

        expected = 3
        actual = qm.complex_logic()

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
