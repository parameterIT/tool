#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser, Node


class Method_Length:
    def __init__(self, src: Path):
        self._py_language = Language("./build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)
        self.src_root = src

    def method_length(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = self._parser.parse(bytes(f.read(), "utf8"))
                query = self._py_language.query(
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
        return count


ml: Method_Length = Method_Length(
    src=Path("./byoqm/")
)  # Path to user src_root, our project as dummy value.
print(ml.method_length())
