import tree_sitter

from pathlib import Path
from typing import Dict

_TREESITTER_BUILD: Path = Path("build/my-languages.so")

_UNKNOWN_ENCODING = "unknown"

_PYTHON = "python"
_C_SHARP = "c_sharp"
_JAVA = "java"
_UNKNOWN_LANGUAGE = "unknown"

_LANGUAGES: Dict[str, tree_sitter.Language] = {
    _PYTHON: tree_sitter.Language(_TREESITTER_BUILD, _PYTHON),
    _C_SHARP: tree_sitter.Language(_TREESITTER_BUILD, _C_SHARP),
    _JAVA: tree_sitter.Language(_TREESITTER_BUILD, _JAVA),
}

_PYTHON_PARSER = tree_sitter.Parser()
_PYTHON_PARSER.set_language(_LANGUAGES[_PYTHON])

_C_S_PARSER = tree_sitter.Parser()
_C_S_PARSER.set_language(_LANGUAGES[_C_SHARP])

_JAVA_PARSER = tree_sitter.Parser()
_JAVA_PARSER.set_language(_LANGUAGES[_JAVA])

_PARSERS: Dict[str, tree_sitter.Parser] = {
    _PYTHON: _PYTHON_PARSER,
    _C_SHARP: _C_S_PARSER,
    _JAVA: _JAVA_PARSER,
}

_ASTS: Dict[str, tree_sitter.Tree] = {
        # Intentionally empty
}

def get_ast(self, for_file: FileInfo) -> tree_sitter.Tree:
    """
    get_ast checks if an AST for the path already has been computed, and returns that
    AST if it is the case. Otherwise, it will parse the file to a tree_sitter AST
    and return that tree.
    """
    try:
        ast = _ASTS[for_file.file_path]
    except KeyError:
        _ASTS[for_file.file_path] = self._parse_ast(for_file)
        ast = _ASTS[for_file.file_path]
    finally:
        return ast
