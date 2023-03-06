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


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


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
    query = PY_LANGUAGE.query(
        """
            (module [
            (if_statement 
                consequence: (block) @cons
                    )
            (if_statement 
                consequence: (block) @cons
                alternative: (_ [body: (block) consequence: (block) ] @cons) 
                    )
            (while_statement body: (block) @cons)
            (for_statement body: (block) @cons)]
            )
            
            (function_definition
            body: (block [
                (if_statement 
                    consequence: (block) @cons
                        )
                (if_statement 
                    consequence: (block) @cons
                    alternative: (_ [body: (block) consequence: (block)] @cons)
                        )
                (while_statement body: (block) @cons)
                (for_statement body: (block) @cons)])
            )
                """
    )
    inital_nodes = unique(query.captures(tree.root_node))
    sub_node_query = PY_LANGUAGE.query(
        """
            (_ [
            (if_statement 
                consequence: (block) @cons
                    )
            (if_statement 
                consequence: (block) @cons
                alternative: (_ [body: (block) consequence: (block) ] @cons) 
                    )
            (while_statement body: (block) @cons)
            (for_statement body: (block) @cons)]
            )
                """
    )
    for node, _ in inital_nodes:
        found = False
        nodes2 = sub_node_query.captures(node)
        for node2, _ in nodes2:
            if found:
                break
            nodes3 = sub_node_query.captures(node2)
            for node3, _ in nodes3:
                if found:
                    break
                if len(sub_node_query.captures(node3)) > 0:
                    count += 1
                    found = True
                    
    return count


print(parse())
