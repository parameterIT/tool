import unittest

import tree_sitter

from core.source_repository.source_repository import SourceRepository
from pathlib import Path


class TestSourceRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.source_repository = SourceRepository(
            Path("core/source_repository/test/data")
        )

    def test_get_ast_given_a_child_file_returns_a_tree_sitter_ast(self):
        target = self.source_repository.files[
            Path("./core/source_repository/test/data/a_file.py")
        ]
        actual = self.source_repository.get_ast(target)

        self.assertIsInstance(actual, tree_sitter.Tree)

    def test_get_ast_returns_tree_with_2_elements(self):
        target = self.source_repository.files[
            Path("./core/source_repository/test/data/a_file.py")
        ]
        tree = self.source_repository.get_ast(target)
        actual = len(tree.root_node.children)
        self.assertEqual(actual, 2)

    def test_source_repository_finds_two_files(self):
        actual = len(self.source_repository.files)
        expected = 2

        self.assertEqual(actual, expected)
