#!/usr/bin/env python
from pathlib import Path
import ast
from tree_sitter import Language, Parser, Node

class Return_Statements:
    def __init__(self, src: Path):
        self._py_language = Language("./build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)
        self.src_root = src

    def return_statements(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = ast.parse(f.read())
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        rs = sum(
                            isinstance(subexp, ast.Return) for subexp in ast.walk(node)
                        )
                        if rs > 4:
                            count += 1
        py_files.close()
        return count

rs: Return_Statements = Return_Statements(
    src=Path("./byoqm/")
)  # Path to user src_root, our project as dummy value.
print(rs.return_statements())