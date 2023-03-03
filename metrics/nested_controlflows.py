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


def parse():
    count = 0
    if src.is_file():
        with src.open() as f:
            count = _parse(f)
    else:
        py_files = src.glob("**/*.py")
        for file in py_files:
            with open(file) as f:
                count += _parse(f)
    return count


def _parse(file) -> int:
    count = 0
    tree = parser.parse(bytes(file.read(), "utf-8"))
    queue = tree.root_node.children
    while len(queue) != 0:
        current = queue.pop(0)
        if _is_control_flow(current) and _can_go_three_down(current, 1):
            count += 1
        else:
            for child in current.children:
                queue.append(child)
    return count


def _can_go_three_down(fromNode, depth) -> bool:
    if depth >= 3:
        return True

    for child in fromNode.children:
        if child.type == "block" or _is_control_flow(child):
            # Check for block as a precaution, because tree-sitter has a block
            # as child following control-flow statements
            return _can_go_three_down(child, depth + 1)
        elif child.type == "elif_clause":
            # elif_clause is a child of an if_statement in tree_sitter, but in code
            # nesting levels a sibling of the if_statement, so don't increment
            # depth
            return _can_go_three_down(child, depth)
        elif child.type == "else_clause":
            # same as elif but for else, this doesn't work
            # Chris's theory: child.type == block somehow prevents ever reaching
            # this branch
            return _can_go_three_down(child, depth)
        elif child.type == "case_clause":
            # same as elif but for cases in a match statement
            return _can_go_three_down(child, depth)
    return False


def _is_control_flow(node) -> bool:
    CONTROL_FLOW_STMTS = (
        "if_statement",
        "for_statement",
        "while_statement",
        "match_statement",
    )
    return node.type in CONTROL_FLOW_STMTS


print(parse())
