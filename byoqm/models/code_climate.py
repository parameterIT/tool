from typing import Dict, List
import ast
import os
from defusedxml.ElementTree import parse
from datetime import date
import csv
from pathlib import Path
import os

from tree_sitter import Language, Parser, Node

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
            "method length": self.method_length,
            "return statements": self.return_statements,
            "identical blocks of code": self.identical_blocks_of_code,
            "argument count": self.argument_count,
            "method count": self.method_count,
            "complex logic": self.complex_logic,
        }
        return model

    def save_to_csv(self, path="./output"):
        file_location = path + "/" + str(date.today()) + ".csv"
        if not os.path.exists(path):
            os.mkdir(path)
        with open(file_location, "w") as file:
            writer = csv.writer(file)
            dict = self.getDesc()
            writer.writerow(["Metric", "Value"])
            for key in dict:
                writer.writerow([key, dict[key]()])

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
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = self._parser.parse(bytes(f.read(), "utf8"))
                query = self._py_language.query(
                    """
                        (_
                            condition: (boolean_operator) @function.boolean_operator)
                        """
                )
                captures = query.captures(tree.root_node)
                for capture in captures:
                    # initial count is always at least 2 (right and left)
                    identifier_count = 2
                    node = capture[0]
                    while node.child_by_field_name("left").type != "identifier":
                        identifier_count += 1
                        node = node.child_by_field_name("left")
                    if identifier_count > 2:
                        count += 1
        py_files.close()
        return count

    def file_length(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                loc = sum(1 for line in f if line.rstrip())
                if loc > 250:
                    count += 1
        py_files.close()
        return count

    def identical_blocks_of_code(self) -> int | float:
        files = [str(file) for file in self.src_root.glob("**/*.py")]
        filestring = f"{files}"
        filestring = filestring[1 : len(filestring) - 1]
        os.system(
            f"metrics/cpd/bin/run.sh cpd --minimum-tokens 5 --skip-lexical-errors --dir {filestring} --format xml > out/result.xml"
        )
        et = parse("out/result.xml")
        count = 0
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
        pass

    def return_statements(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        rs = sum(
                            isinstance(subexp, ast.Return) for subexp in ast.walk(node)
                        )
                        if rs > 4:
                            count += 1
        py_files.close()
        return count
        pass

    def similar_blocks_of_code(self) -> int | float:
        return 3
