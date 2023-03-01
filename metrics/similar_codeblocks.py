#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser
import sys


def parse_src_root() -> Path:
    if len(sys.argv) == 1:
        print("Make sure to provide the path to source code")
        exit(1)

    path_to_src = Path(sys.argv[1])
    if not path_to_src.exists():
        print(f"The source code at {path_to_src.resolve()} does not exist")
        exit(1)

    return path_to_src


PY_LANGUAGE = Language("./build/my-languages.so", "python")
parser = Parser()
parser.set_language(PY_LANGUAGE)
src = parse_src_root()
py_files = src.glob("**/*.py")
print(2)  # Missing logic
