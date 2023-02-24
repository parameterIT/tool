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
        }
        return model

    def maintainability(self):
        return 7 + self.duplication()

    def duplication(self) -> int | float:
        return self.identical_blocks_of_code() + self.similar_blocks_of_code()

    def cognitive_complexity(self):
        with self.results.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["metric"] == "argument_count":
                    return int(row["value"])
            #return int(reader["argument_count"])
        pass

    def cyclomatic_complexity(self):
        pass

    def identical_blocks_of_code(self) -> int | float:
        return 2

    def method_complexity(self):
        pass

    def nested_control_flow(self):
        pass

    def similar_blocks_of_code(self) -> int | float:
        return 3
