#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser
import ast


class Argument_Count:
    def __init__(self, src: Path):
        self._py_language = Language("../build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)
        self.src_root = src

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


ac: Argument_Count = Argument_Count(
    src=Path("../byoqm/")
)  # Path to user src_root, our project as dummy value.
print("Argument count violations,", ac.argument_count())
