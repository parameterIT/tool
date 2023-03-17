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

    def test_get_ast_returns_tree_with_2_elements(self):
        target = Path("./byoqm/source_coordinator/test/data/a_file.py")
        tree = self.source_coordinator.getAst(target)
        actual = len(tree.root_node.children)
        self.assertEqual(actual, 2)

    def test_new_source_coordinator_findes_c_sharp_files(self):
        new_coordinator = SourceCoordinator(
            Path("byoqm/source_coordinator/test/data"), "c_sharp"
        )
        actual = new_coordinator.src_paths

        self.assertEqual(
            actual, [Path("byoqm/source_coordinator/test/data/a_nother_file.cs")]
        )
