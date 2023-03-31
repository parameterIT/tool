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
                "identical_code": "./metrics/identical_codeblocks.py",
                "similar_code": "./metrics/similar_codeblocks.py",
                "nested_control_flow": "./metrics/nested_controlflows.py",
                "cognitive_complexity": "./metrics/cognitive_complexity.py",
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
            results["identical_code"].get_frequency()
            + results["similar_code"].get_frequency()
        )

    def cognitive_complexity(self, results: Dict):
        return results["cognitive_complexity"].get_frequency()


model = CodeClimate()
