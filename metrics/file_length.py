#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser


class File_Length:
    def __init__(self, src: Path):
        self._py_language = Language("./build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)
        self.src_root = src

    def file_length(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                loc = sum(1 for line in f if line.rstrip())
                if loc > 250:
                    count += 1
        py_files.close()
        return count


fl: File_Length = File_Length(
    src=Path("./byoqm/")
)  # Path to user src_root, our project as dummy value.
print(fl.file_length())
