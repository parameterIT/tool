from typing import Dict

from tree_sitter import Language, Parser

from modu.qualitymodel.qualitymodel import QualityModel


class TesterModel(QualityModel):
    def __init__(self):
        self._py_language = Language("build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)

    def get_desc(self) -> Dict:
        model = {
            "metrics": {
                "method_count": "./metrics/method_count.py",
            },
            "aggregations": {
                "maintainability": self.maintainability,
            },
        }
        return model

    def maintainability(self, results: Dict) -> int | float:
        return results["method_count"].outcome


model = TesterModel()
