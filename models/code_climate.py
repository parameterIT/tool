from typing import Dict

from tree_sitter import Language, Parser

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):

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
                "cyclomatic_complexity": self.cyclomatic_complexity,
                "structural_issues": self.structural_issues,
                "cognitive_complexity": self.cognitive_complexity,
                "duplication": self.duplication,
                "maintainability": self.maintainability,
            },
        }
        return model

    def maintainability(self, results: Dict) -> int | float:
        return (
            results["duplication"]
            + results["cognitive_complexity"]
            + results["structural_issues"]
            + results["cyclomatic_complexity"]
        )

    def duplication(self, results: Dict) -> int | float:
        return results["identical_blocks_of_code"] + results["similar_blocks_of_code"]

    def cognitive_complexity(self, results: Dict):
        return results["complex_logic"] + results["nested_controlflows"]

    def structural_issues(self, results: Dict):
        return (
            results["argument_count"] + results["file_length"] + results["method_count"]
        )

    def cyclomatic_complexity(self, results: Dict):
        return results["return_statements"]


model = CodeClimate()
