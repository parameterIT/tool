from typing import Dict

from core.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    # Arbitrary choice of 30 minutes implementation time per line
    _LINE_IMPLEMENTATION_TIME = 30
    # Code Climate reports 45 minutes to fix when 3 over the allowed cognitive complexity
    _COGNITIVE_COMPLEXITY_REMEDIATION_COST = 45
    # Too many return statements is reported as 30 minutes to fix
    _RETURN_STATEMENTS_REMEDIATION_COST = 30
    # Nested control flow is reported as taking 45 minutes to fix
    _NESTED_CONTROL_FLOW_REMEDIATION_COST = 60
    # When argument count is exactly one over the threshhold (5) it takes 35 minutes
    # to fix It seems to scale with 10 minutes per argument hat is over when it is (6)
    # then it takes 45 minutes to fix
    _ARGUMENT_COUNT_REMEDIATION_COST = 35
    # When the method is 9 lines over 25, Code Climate reports that it takes 1 hour to fix
    _METHOD_LINES_REMEDIATION_COST = 60
    # When the file is exactly 1 line over 250, Code Climate reports that it will take 2 hours to fix
    _FILE_LINES_REMEDIATION_COST = 120
    # When there is code duplication in 2 places, Code Climate reports that it will take 1 hour to fix
    # It does, however, appear that they account for the size of the code snippet somehow as they sometimes
    # report 45, 50 mminutes
    _IDENTICAL_CODE_REMEDIATION_COST = 60
    _SIMILAR_CODE_REMEDIATION_COST = 60

    def get_desc(self) -> Dict:
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
                "code_size": "./metrics/code_size.py",
            },
            "aggregations": {
                "complexity": self.complexity,
                "duplication": self.duplication,
                "maintainability": self.maintainability,
            },
        }
        return model

    def maintainability(self, results: Dict) -> str:
        # https://docs.codeclimate.com/docs/maintainability-calculation
        code_size: int = results["code_size"]
        implementation_time: int = code_size * self._LINE_IMPLEMENTATION_TIME
        technical_debt = self.complexity_remediation(results)
        +self.duplication_remediation(results)
        tech_debt_ratio: float = technical_debt / implementation_time

        return self._map_to_letter(tech_debt_ratio)

    def _map_to_letter(self, tech_debt_ratio: float) -> str:
        # Intervals are taken from Pfeiffers and Lungu's Paper:
        # Technical Debt and Maintainability: How do tools measure it?
        if 0 <= tech_debt_ratio <= 0.05:
            return "A"
        elif 0.05 < tech_debt_ratio <= 0.1:
            return "B"
        elif 0.1 < tech_debt_ratio <= 0.2:
            return "C"
        elif 0.2 < tech_debt_ratio <= 0.5:
            return "D"
        else:
            return "F"

    def complexity_remediation(self, results: Dict) -> int:
        return (
            results["cognitive_complexity"].outcome
            * self._COGNITIVE_COMPLEXITY_REMEDIATION_COST
            + results["return_statements"].outcome
            * self._RETURN_STATEMENTS_REMEDIATION_COST
            + results["nested_control_flow"].outcome
            * self._NESTED_CONTROL_FLOW_REMEDIATION_COST
            + results["argument_count"].outcome * self._ARGUMENT_COUNT_REMEDIATION_COST
            + results["method_lines"].outcome * self._METHOD_LINES_REMEDIATION_COST
            + results["file_lines"].outcome * self._FILE_LINES_REMEDIATION_COST
        )

    def complexity(self, results: Dict) -> int | float:
        return (
            results["cognitive_complexity"].outcome
            + results["return_statements"].outcome
            + results["nested_control_flow"].outcome
            + results["argument_count"].outcome
            + results["method_lines"].outcome
            + results["file_lines"].outcome
        )

    def duplication(self, results: Dict) -> int | float:
        return results["identical_code"].outcome + results["similar_code"].outcome

    def duplication_remediation(self, results: Dict) -> int:
        return (
            results["identical_code"].outcome * self._IDENTICAL_CODE_REMEDIATION_COST
            + results["similar_code"].outcome * self._SIMILAR_CODE_REMEDIATION_COST
        )


model = CodeClimate()
