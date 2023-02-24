#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser

class Identical_Codeblocks:
    def __init__(self, src: Path):
        self._py_language = Language("./build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)
        self.src_root = src
    
    def identical_codeblocks(self):
        return 2

ic: Identical_Codeblocks = Identical_Codeblocks(
    src=Path("./byoqm/")
)  # Path to user src_root, our project as dummy value.
print(ic.identical_codeblocks())