from typing import Dict

from tree_sitter import Language, Parser

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    def getDesc(self) -> Dict:
        model = {
            "metrics": {
                "method_lines": "./metrics/method_length.py",
                "file_lines": "./metrics/file_length.py",
                "argument_count": "./metrics/argument_count.py",
                "complex_logic": "./metrics/complex_logic.py",
                "method_count": "./metrics/method_count.py",
                "return_statements": "./metrics/return_statements.py",
                "identical-code": "./metrics/identical_codeblocks.py",
                "similar-code": "./metrics/similar_codeblocks.py",
                "nested_control_flow": "./metrics/nested_controlflows.py",
                "breaks_in_linear_flow": "./metrics/breaks_in_linear_flow.py",
            },
            "aggregations": {
                "cognitive_complexity": self.cognitive_complexity,
                "Complexity": self.complexity,
                "Duplication": self.duplication,
            },
        }
        return model

    def complexity(self, results: Dict) -> int | float:
        return (
            results["cognitive_complexity"]
            + len(results["return_statements"])
            + len(results["nested_control_flow"])
            + len(results["argument_count"])
            + len(results["method_lines"])
            + len(results["file_lines"])
        )

    def duplication(self, results: Dict) -> int | float:
        return len(results["identical-code"]) + len(results["similar-code"])

    def cognitive_complexity(self, results: Dict):
        return len(results["complex_logic"]) + len(results["breaks_in_linear_flow"])


model = CodeClimate()
