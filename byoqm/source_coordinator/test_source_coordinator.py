import unittest

import tree_sitter

from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from pathlib import Path


class TestSourceCoordinator(unittest.TestCase):
    def setUp(self) -> None:
        self.source_coordinator = SourceCoordinator(
            Path("byoqm/source_coordinator/test/data"), "python"
        )

    def test_get_ast_given_a_child_file_returns_a_tree_sitter_ast(self):
        target = Path("./byoqm/source_coordinator/test/data/a_file.py")
        actual = self.source_coordinator.getAst(target)

        self.assertIsInstance(actual, tree_sitter.Tree)

    def test_get_ast_given_a_sibling_file_fails(self):
        target = Path("./byoqm/source_coordinator/source_coordinator.py")
        self.assertRaises(ValueError, self.source_coordinator.getAst, target)
