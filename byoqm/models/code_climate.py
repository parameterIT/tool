from typing import Dict
import subprocess
from typing import Dict
import ast
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
                if row["Metric"] == "identical_blocks_of_code":
                    sum += int(row["Value"])
                if row["Metric"] == "similar_blocks_of_code":
                    sum += int(row["Value"])
            return sum

    def cognitive_complexity(self) -> int | float:
        with self.results.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Metric"] == "complex_logic":
                    return int(row["Value"])

    def structural_issues(self):
        with self.results.open() as f:
            reader = csv.DictReader(f)
            sum = 0
            for row in reader:
                if row["Metric"] == "argument_count":
                    sum += int(row["Value"])
                if row["Metric"] == "file_length":
                    sum += int(row["Value"])
                if row["Metric"] == "method_count":
                    sum += int(row["Value"])
            return sum

    def cyclomatic_complexity(self):
        with self.results.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Metric"] == "return_statements":
                    return int(row["Value"])

    def similar_blocks_of_code(self) -> int | float:
        return 3
