import os
import unittest
import tree_sitter
from metrics.util.query_translations import translate_to

from pathlib import Path
from byoqm.metric.metric import Metric

from byoqm.source_repository.source_repository import SourceRepository
from metrics.cognitive_complexity import CognitiveComplexity


class TestCognitiveComplexity(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository: SourceRepository = SourceRepository(
            Path("./metrics/test/data/test_cognitive_complexity/test_recursion")
        )
        self._metric: Metric = CognitiveComplexity()
        self._metric._source_repository = self._source_repository

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())

    def test_recursion_returns_3(self):
        result = self._metric.run()
        actual = result.outcome
        expected = 3
        self.assertEqual(actual, expected)

        locations = result.get_violation_locations()
        expected_locations = [
            (
                "metrics/test/data/test_cognitive_complexity/test_recursion/data_recursion.py",
                1,
                8,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_recursion/data_recursion.java",
                5,
                13,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_recursion/data_recursion.cs",
                5,
                15,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)

    def test_breaks_in_linear_flow_returns_3(self):
        new_source_repository = SourceRepository(
            Path(
                "./metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow"
            )
        )
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 3
        self.assertEqual(actual, expected)

        locations = result.get_violation_locations()
        expected_locations = [
            (
                "metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow/data_breaks_in_linear_flow.cs",
                10,
                49,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow/data_breaks_in_linear_flow.py",
                1,
                25,
            ),
            (
                "metrics/test/data/test_cognitive_complexity/test_breaks_in_linear_flow/data_breaks_in_linear_flow.java",
                5,
                42,
            ),
        ]
        self.assertCountEqual(locations, expected_locations)

    def test_nesting_returns_5(self):
        new_source_repository = SourceRepository(
            Path(
                "./metrics/test/data/test_cognitive_complexity/test_nested_controlflows"
            )
        )
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        print("---------------------------------------")
        actual = 0
        for (
            file_path,
            file_info,
        ) in cognitive_complexity._source_repository.files.items():
            print(file_path)
            ast: tree_sitter.Tree = cognitive_complexity._source_repository.get_ast(
                file_info
            )
            tree_sitter_language = (
                cognitive_complexity._source_repository.tree_sitter_languages[
                    file_info.language
                ]
            )

            initial_nodes_query_str = (
                f"""{translate_to[file_info.language]["function"]} @func"""
            )
            if file_info.language == "c_sharp" or file_info.language == "java":
                initial_nodes_query_str += (
                    f"""{translate_to[file_info.language]["constructor"]} @cons"""
                )
            query_initial_nodes = tree_sitter_language.query(initial_nodes_query_str)
            initial_nodes = query_initial_nodes.captures(ast.root_node)
            for node, _ in initial_nodes:
                print(node)
                count = cognitive_complexity._count_nesting(node, file_info)
                print(count)
                actual += count

        expected = 5
        self.assertEqual(actual, expected)

    def test_cognitive_complexity_returns_12(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_cognitive_complexity")
        )
        cognitive_complexity = CognitiveComplexity()
        cognitive_complexity._source_repository = new_source_repository
        result = cognitive_complexity.run()
        actual = result.outcome
        expected = 12
        self.assertEqual(actual, expected)
