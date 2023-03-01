#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser, Node
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
count = 0
for file in py_files:
    with open(file) as f:
        tree = parser.parse(bytes(f.read(), "utf8"))
        query = PY_LANGUAGE.query(
            """
                    (function_definition
                        body: (block) @function.block)
                    """
        )
        captures = query.captures(tree.root_node)
        for node in captures:
            n = node[0]
            length = (
                n.end_point[0] - n.start_point[0] + 1
            )  # e.g. sp 1, ep 7 -> 7 - 1 = 6 + 1 = 7
            if length > 25:
                count += 1
py_files.close()

print(count)
