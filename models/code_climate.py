from typing import Dict

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
                "recursion": "./metrics/recursion.py",
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
            + results["return_statements"].get_frequency()
            + results["nested_control_flow"].get_frequency()
            + results["argument_count"].get_frequency()
            + results["method_lines"].get_frequency()
            + results["file_lines"].get_frequency()
        )

    def duplication(self, results: Dict) -> int | float:
        return (
            results["identical-code"].get_frequency()
            + results["similar-code"].get_frequency()
            + results["recursion"].get_frequency()
        )

    def cognitive_complexity(self, results: Dict):
        return results["complex_logic"].get_frequency() + results["breaks_in_linear_flow"].get_frequency()


model = CodeClimate()
