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


def parse():
    count = 0
    src = parse_src_root()
    if src.is_file():
        with src.open() as f:
            count = _parse(f)
    else:
        py_files = src.glob("**/*.py")
        for file in py_files:
            with open(file) as f:
                count += _parse(f)
        py_files.close()
    return count


def _parse(file):
    count = 0
    loc = sum(1 for line in file if line.rstrip())
    if loc > 250:
        count += 1
    return count


print(parse())
