from typing import Dict

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    def getDesc(self) -> Dict:
        model = {
            "maintainability": self.maintainability,
            "duplication": self.duplication,
            "lines of code": self.file_length,
        }
        return model

    def maintainability(self):
        return 7 + self.duplication()

    def duplication(self) -> int | float:
        return self.identical_blocks_of_code() + self.similar_blocks_of_code()

    def cognitive_complexity(self):
        pass

    def cyclomatic_complexity(self):
        pass

    def argument_count(self):
        pass

    def complex_logic(self):
        pass

    def file_length(self):
        src_files = list(self.src_root.glob("**/*.py"))
        count = 0
        for file in src_files:
            loc = sum(1 for line in open(file))
            if loc > 250:
                count += 1
        return count

    def identical_blocks_of_code(self) -> int | float:
        return 2

    def method_complexity(self):
        pass

    def method_count(self):
        pass

    def method_length(self):
        pass

    def nested_control_flow(self):
        pass

    def return_statements(self):
        pass

    def similar_blocks_of_code(self) -> int | float:
        return 3
