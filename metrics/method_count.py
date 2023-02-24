#!/usr/bin/env python
import ast
from pathlib import Path
from tree_sitter import Language, Parser

class Method_Count:
    def __init__(self, src : Path):
            self._py_language = Language("../build/my-languages.so", "python")
            self._parser = Parser()
            self._parser.set_language(self._py_language)
            self.src_root = src
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

mc : Method_Count = Method_Count(src = Path("../byoqm/")) #Path to user src_root, our project as dummy value.
print("Method count violations,",mc.method_count())