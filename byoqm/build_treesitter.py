from tree_sitter import Language

Language.build_library("build/my-languages.so", ["grammars/tree-sitter-python"])
