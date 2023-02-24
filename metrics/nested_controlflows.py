#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser

class Nested_Controlflows:
    def __init__(self, src: Path):
        self._py_language = Language("./build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)
        self.src_root = src
    
    def nested_controlflows(self):
        return 4

ic: Nested_Controlflows = Nested_Controlflows(
    src=Path("./byoqm/")
)  # Path to user src_root, our project as dummy value.
print(ic.nested_controlflows())