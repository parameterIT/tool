from typing import Dict, List
import ast

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    def getDesc(self) -> Dict:
        model = {
            "maintainability": self.maintainability,
            "duplication": self.duplication,
            "lines of code": self.file_length,
            "return statements": self.return_statements,
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
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                loc = sum(1 for line in f)
                if loc > 250:
                    count += 1
        py_files.close()
        return count

    def identical_blocks_of_code(self) -> int | float:
        return 2

    def method_complexity(self):
        pass

    def method_count(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                mc = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
                if mc > 20:
                    count += 1
        py_files.close
        return count

    def method_length(self):
        pass

    def nested_control_flow(self):
        pass

    def return_statements(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f: 
                tree = ast.parse(f.read())
                for exp in tree.body:
                    if isinstance(exp, ast.FunctionDef):
                        print(exp)
                        
                        if exp.body == None:  
                            continue
                        rc = sum(isinstance(subExp, ast.Return) for subExp in exp.body)
                        print (rc)
                        if rc > 4: 
                            count += 1
        py_files.close()
        return count
        pass

    def similar_blocks_of_code(self) -> int | float:
        return 3

    def return_count_per_node(nodes : List[ast.stmt]) -> int | float:
        if nodes.count() == 0:
            return 0
        sum = 0
        for element in nodes:
            if element == None:
                continue
            