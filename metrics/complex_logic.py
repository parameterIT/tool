#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser


class Complex_Logic:
    def __init__(self, src: Path):
        self._py_language = Language("../build/my-languages.so", "python")
        self._parser = Parser()
        self._parser.set_language(self._py_language)
        self.src_root = src

    def complex_logic(self):
        py_files = self.src_root.glob("**/*.py")
        count = 0
        for file in py_files:
            with open(file) as f:
                tree = self._parser.parse(bytes(f.read(), "utf8"))
                query = self._py_language.query(
                    """
                        (_
                            condition: (boolean_operator) @function.boolean_operator)
                        """
                )
                captures = query.captures(tree.root_node)
                for capture in captures:
                    # initial count is always at least 2 (right and left)
                    identifier_count = 2
                    node = capture[0]
                    while node.child_by_field_name("left").type != "identifier":
                        identifier_count += 1
                        node = node.child_by_field_name("left")
                    if identifier_count > 2:
                        count += 1
        py_files.close()
        return count


cl: Complex_Logic = Complex_Logic(
    src=Path("../byoqm/")
)  # Path to user src_root, our project as dummy value.
print("Complex logic violations,", cl.complex_logic())
