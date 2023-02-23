from typing import Dict, List
import ast

from tree_sitter import Language, Parser
import tree_sitter

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    def __init__(self):
        self._py_language = Language("build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)

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
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                for exp in tree.body:
                    if not isinstance(exp, ast.FunctionDef):
                        continue
                    if len(exp.args.args) > 4:
                        count += 1
        py_files.close()
        return count

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
        py_files.close()
        return count

    def method_length(self):
        pass

    def nested_control_flow(self):
        # 4 or more levels of nesting should be counted up
        # if, while, for
        tree = self._parser.parse(
            bytes(
                """
if i == 0:
    if i == 1:
    	if i == 2:
            if i < j:
                pass
if x == 0:
	if x == 1:
    	if x == 2:
            if x < z:
                pass
""",
                "utf8",
            )
        )  # end of tree
        root: tree_sitter.Node | None = tree.root_node
        violations = self._nested_control_flow(root, 0, 0)
        return violations

    def _nested_control_flow(
        self, current: tree_sitter.Node | None, depth: int, violations: int
    ) -> int:
        print(current, depth)
        if current == None:
            return violations

        if current.type == "if":
            depth += 1

        if depth >= 4:
            return violations + 1

        if current.next_sibling != None:
            current = current.next_sibling
            return self._nested_control_flow(current, depth, violations)
        elif current.child_count >= 1:
            # walk across all children
            for child in current.children:
                return self._nested_control_flow(child, depth + 1, violations)
            else:
                return violations
        elif current.next_sibling == None:
            return violations

    def return_statements(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                for exp in tree.body:
                    if isinstance(exp, ast.FunctionDef):
                        rs = sum(
                            isinstance(subexp, ast.Return) for subexp in ast.walk(exp)
                        )
                        if rs > 4:
                            count += 1
        py_files.close()
        return count
        pass

    def similar_blocks_of_code(self) -> int | float:
        return 3
