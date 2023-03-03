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

src_root = parse_src_root()

py_files = src_root.glob("**/*.py")


def parse():
    count = 0
    # single file path
    if src_root.is_file():
        with src_root.open() as f:
            count = _parse(f)
    else:
        py_files = src_root.glob("**/*.py")

        for file in py_files:
            with open(file) as f:
                count += _parse(f)
        py_files.close()
    return count


def _parse(file):
    tree = parser.parse(bytes(file.read(), "utf8"))
    query = PY_LANGUAGE.query(
        """
            (_
                condition: (boolean_operator) @function.boolean_operator)
            (_
                right: (boolean_operator) @function.boolean_operator)

            """
    )
    captures = query.captures(tree.root_node)
    count = 0
    for capture in captures:
        # initial count is always at least 2 (right and left)
        boolean_count = 2
        node = capture[0]
        while node.child_by_field_name("left").type == "boolean_operator":
            boolean_count += 1
            node = node.child_by_field_name("left")
            # change the value below to a parameter when parameterizing
        if boolean_count > 2:
            count += 1
    return count


print(parse())
