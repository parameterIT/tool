from typing import Dict
import ast
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
            "method_length": "./metrics/method_length.py",
            "file_length": "./metrics/file_length.py",
            "argument_count": "./metrics/argument_count.py",
            "complex_logic": "./metrics/complex_logic.py",
            "method_count": "./metrics/method_count.py",
            "return_statements": "./metrics/return_statements.py",
            "identical_blocks_of_code": "./metrics/identical_codeblocks.py",
            "similar_blocks_of_code": "./metrics/similar_codeblocks.py",
            "nested_controlflows": "./metrics/nested_controlflows.py",
        }
        return model

    def maintainability(self):
        return self.duplication() + self.cognitive_complexity() + self.structural_issues() + self.cyclomatic_complexity()

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