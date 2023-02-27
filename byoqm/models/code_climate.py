from typing import Dict
from io import StringIO
import subprocess
from typing import Dict
import ast
from defusedxml.ElementTree import parse
import csv

from tree_sitter import Language, Parser, Node

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    def __init__(self):
        self._py_language = Language("build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)

    def getDesc(self) -> Dict:
        model = {
            "metrics": {
                "method_length": "./metrics/method_length.py",
                "file_length": "./metrics/file_length.py",
                "argument_count": "./metrics/argument_count.py",
                "complex_logic": "./metrics/complex_logic.py",
                "method_count": "./metrics/method_count.py",
                "return_statements": "./metrics/return_statements.py",
                "identical_blocks_of_code": "./metrics/identical_codeblocks.py",
                "similar_blocks_of_code": "./metrics/similar_codeblocks.py",
                "nested_controlflows": "./metrics/nested_controlflows.py",
            },
            "aggregations": {
                "quality": self.maintainability,
                "maintainability": self.maintainability,
                "duplication": self.duplication,
                "cognitive complexity": self.cognitive_complexity,
                "structural issues": self.structural_issues,
                "cyclomatic complexity": self.cyclomatic_complexity,
            },
        }
        return model

    def get_aggregated_results(self):
        return self.maintainability()

    def maintainability(self):
        return (
            self.duplication()
            + self.cognitive_complexity()
            + self.structural_issues()
            + self.cyclomatic_complexity()
        )

    def duplication(self) -> int | float:
        with self.results.open() as f:
            reader = csv.DictReader(f)
            sum = 0
            for row in reader:
                if row["metric"] == "identical_blocks_of_code":
                    sum += int(row["value"])
                if row["metric"] == "similar_blocks_of_code":
                    sum += int(row["value"])
            return sum

    def cognitive_complexity(self) -> int | float:
        with self.results.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["metric"] == "complex_logic":
                    return int(row["value"])

    def structural_issues(self):
        with self.results.open() as f:
            reader = csv.DictReader(f)
            sum = 0
            for row in reader:
                if row["metric"] == "argument_count":
                    sum += int(row["value"])
                if row["metric"] == "file_length":
                    sum += int(row["value"])
                if row["metric"] == "method_count":
                    sum += int(row["value"])
            return sum

    def cyclomatic_complexity(self):
        with self.results.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["metric"] == "return_statements":
                    return int(row["value"])

    def complex_logic(self):
        count = 0
        # single file path
        if self.src_root.is_file():
            with self.src_root.open() as f:
                count = self._complex_logic(f)
        else:
            py_files = self.src_root.glob("**/*.py")

            for file in py_files:
                with open(file) as f:
                    count += self._complex_logic(f)
            py_files.close()
        return count

    def _complex_logic(self, f):
        tree = self._parser.parse(bytes(f.read(), "utf8"))
        query = self._py_language.query(
            """
                (_
                    condition: (boolean_operator) @function.boolean_operator)
                (_
                    right: (boolean_operator) @function.boolean_operator)

                """
        )
        captures = query.captures(tree.root_node)
        count = 0
        for capture in captures:
            # initial count is always at least 2 (right and left)
            boolean_count = 2
            node = capture[0]
            while node.child_by_field_name("left").type == "boolean_operator":
                boolean_count += 1
                node = node.child_by_field_name("left")
                # change the value below to a parameter when parameterizing
            if boolean_count > 2:
                count += 1
        return count

    def identical_blocks_of_code(self, tokens) -> int | float:
        files = []
        if self.src_root.is_file():
            files = [str(self.src_root)]
        else:
            files = [str(file) for file in self.src_root.glob("**/*.py")]
        filestring = f"{files}"
        filestring = filestring[1 : len(filestring) - 1]
        count = 0
        res = subprocess.run(
            f"metrics/cpd/bin/run.sh cpd --minimum-tokens {tokens} --skip-lexical-errors --dir {filestring} --format xml",
            shell=True,
            capture_output=True,
            text=True,
        )
        et = parse(StringIO(res.stdout))
        for child in et.getroot():
            if child.tag == "duplication":
                count += 1
        return count

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
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = self._parser.parse(bytes(f.read(), "utf8"))
                query = self._py_language.query(
                    """
                        (function_definition
                            body: (block) @function.block)
                        """
                )
                captures = query.captures(tree.root_node)
                for node in captures:
                    n = node[0]
                    length = (
                        n.end_point[0] - n.start_point[0] + 1
                    )  # e.g. sp 1, ep 7 -> 7 - 1 = 6 + 1 = 7
                    if length > 25:
                        count += 1
        py_files.close()
        return count

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
        count = 0
        tree = self._parser.parse(bytes(f.read(), "utf-8"))
        queue = tree.root_node.children
        while len(queue) != 0:
            current = queue.pop(0)
            if self._is_control_flow(current) and self._can_go_three_down(current, 1):
                count += 1
            else:
                for child in current.children:
                    queue.append(child)
        return count

    def _can_go_three_down(self, fromNode, depth) -> bool:
        if depth >= 3:
            return True

        for child in fromNode.children:
            if child.type == "block" or self._is_control_flow(child):
                # Check for block as a precaution, because tree-sitter has a block
                # as child following control-flow statements
                return self._can_go_three_down(child, depth + 1)
            elif child.type == "elif_clause":
                # elif_clause is a child of an if_statement in tree_sitter, but in code
                # nesting levels a sibling of the if_statement, so don't increment
                # depth
                return self._can_go_three_down(child, depth)
            elif child.type == "else_clause":
                # same as elif but for else, this doesn't work
                # Chris's theory: child.type == block somehow prevents ever reaching
                # this branch
                return self._can_go_three_down(child, depth)
            elif child.type == "case_clause":
                # same as elif but for cases in a match statement
                return self._can_go_three_down(child, depth)
        return False

    def _is_control_flow(self, node) -> bool:
        CONTROL_FLOW_STMTS = (
            "if_statement",
            "for_statement",
            "while_statement",
            "match_statement",
        )
        return node.type in CONTROL_FLOW_STMTS

    def similar_blocks_of_code(self) -> int | float:
        return 3
