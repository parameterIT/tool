from io import FileIO
from re import DEBUG
from typing import Dict, List
import ast
from test.test_support import sys
import logging

from tree_sitter import Language, Parser
import tree_sitter

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    def __init__(self):
        self._py_language = Language("build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)

    def getDesc(self) -> Dict:
        model = {
            "maintainability": self.maintainability,
            "duplication": self.duplication,
            "lines of code": self.file_length,
            "return statements": self.return_statements,
        }
        return model

    def maintainability(self):
        return 7 + self.duplication()

    def duplication(self) -> int | float:
        return self.identical_blocks_of_code() + self.similar_blocks_of_code()

    def cognitive_complexity(self):
        pass

    def cyclomatic_complexity(self):
        pass

    def argument_count(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                for exp in tree.body:
                    if not isinstance(exp, ast.FunctionDef):
                        continue
                    if len(exp.args.args) > 4:
                        count += 1
        py_files.close()
        return count

    def complex_logic(self):
        pass

    def file_length(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                loc = sum(1 for line in f)
                if loc > 250:
                    count += 1
        py_files.close()
        return count

    def identical_blocks_of_code(self) -> int | float:
        return 2

    def method_complexity(self):
        pass

    def method_count(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                mc = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
                if mc > 20:
                    count += 1
        py_files.close()
        return count

    def method_length(self):
        pass

    def nested_control_flow(self):
        count = 0
        if self.src_root.is_file():
            with self.src_root.open() as f:
                count = self._nested_control_flow(f)
        else:
            py_files = self.src_root.glob("**/*.py")
            for file in py_files:
                with open(file) as f:
                    count += self._nested_control_flow(f)
        return count

    def _nested_control_flow(self, f) -> int:
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger("tester").setLevel(logging.DEBUG)

        count = 0
        tree = self._parser.parse(bytes(f.read(), "utf-8"))
        queue = tree.root_node.children
        while len(queue) != 0:
            current = queue.pop(0)
            if self._is_control_flow_or_extraneous(current) and self._can_go_three_down(
                current, 1
            ):
                count += 1
            else:
                for child in current.children:
                    queue.append(child)
        return count

    # Look for if_statement followed by block, check that block for the next if_statement
    # generalize to look for any _statement followed by block, check that block for _statement
    def _can_go_three_down(self, fromNode, depth) -> bool:
        if depth == 3:
            return True
        else:
            for child in fromNode.children:
                if child.type == "block":
                    return self._can_go_three_down(child, depth)
                if self._is_control_flow(child):
                    return self._can_go_three_down(child, depth + 1)

        return False

    def _is_control_flow(self, node) -> bool:
        return (
            node.type == "if"
            or node.type == "if_statement"
            or node.type == "for_statement"
        )

    def _is_control_flow_or_extraneous(self, node) -> bool:
        return self._is_control_flow(node) or node.type == "block"

    def return_statements(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                for exp in tree.body:
                    if isinstance(exp, ast.FunctionDef):
                        rs = sum(
                            isinstance(subexp, ast.Return) for subexp in ast.walk(exp)
                        )
                        if rs > 4:
                            count += 1
        py_files.close()
        return count
        pass

    def similar_blocks_of_code(self) -> int | float:
        return 3
