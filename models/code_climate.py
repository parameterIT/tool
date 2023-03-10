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
                "cognitive_complexity": self.cognitive_complexity,
                "complexity": self.complexity,
                "duplication": self.duplication,
            },
        }
        return model

    def complexity(self, results: Dict) -> int | float:
        return (
            results["cognitive_complexity"]
            + results["return_statements"]
            + results["nested_controlflows"]
            + results["argument_count"]
            + results["method_length"]
            + results["file_length"]
        )

    def duplication(self, results: Dict) -> int | float:
        return results["identical_blocks_of_code"] + results["similar_blocks_of_code"]

    def cognitive_complexity(self, results: Dict):
        return results["complex_logic"]


model = CodeClimate()
