from typing import Dict, List
import ast
import os
from defusedxml.ElementTree import parse

from tree_sitter import Language, Parser

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    def __init__(self):
        py_language = Language("build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(py_language)

    def getDesc(self) -> Dict:
        model = {
            "maintainability": self.maintainability,
            "duplication": self.duplication,
            "lines of code": self.file_length,
            "return statements": self.return_statements,
            "identical blocks of code": self.identical_blocks_of_code,
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
        files = []
        for file in self.src_root.glob("**/*.py"):
            files.append(str(file))
        filestring = f"{files}"; filestring = filestring[1:len(filestring)-1]
        os.system(f"metrics/cpd/bin/run.sh cpd --minimum-tokens 10 --skip-lexical-errors --dir {filestring} --format xml > out/result.xml")
        et = parse("result.xml")
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
        pass

    def nested_control_flow(self):
        pass

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
