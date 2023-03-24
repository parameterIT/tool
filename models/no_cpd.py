from typing import Dict


from byoqm.qualitymodel.qualitymodel import QualityModel


class NoCpd(QualityModel):
    def __init__(self):
        pass

    def getDesc(self) -> Dict:
        model = {
            "metrics": {
                "method_length": "./metrics/method_length.py",
                "file_length": "./metrics/file_length.py",
                "argument_count": "./metrics/argument_count.py",
                "complex_logic": "./metrics/complex_logic.py",
                "method_count": "./metrics/method_count.py",
                "return_statements": "./metrics/return_statements.py",
                "nested_controlflows": "./metrics/nested_controlflows.py",
            },
            "aggregations": {
                "cyclomatic_complexity": self.cyclomatic_complexity,
                "structural_issues": self.structural_issues,
                "cognitive_complexity": self.cognitive_complexity,
                "maintainability": self.maintainability,
            },
        }
        return model

    def maintainability(self, results: Dict) -> int | float:
        return (
            results["cognitive_complexity"]
            + results["structural_issues"]
            + results["cyclomatic_complexity"]
        )

    def cognitive_complexity(self, results: Dict):
        return (
            results["complex_logic"].get_frequency()
            + results["nested_controlflows"].get_frequency()
        )

    def structural_issues(self, results: Dict):
        return (
            results["argument_count"].get_frequency()
            + results["file_length"].get_frequency()
            + results["method_count"].get_frequency()
        )

    def cyclomatic_complexity(self, results: Dict):
        return results["return_statements"].get_frequency()


model = NoCpd()
