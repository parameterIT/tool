import tree_sitter

from core.source_repository.file_info import FileInfo
from pathlib import Path
from typing import Dict

_TREESITTER_BUILD: Path = Path("build/my-languages.so")


_PYTHON = "python"
_C_SHARP = "c_sharp"
_JAVA = "java"
_UNKNOWN_LANGUAGE = "unknown"

LANGUAGES: Dict[str, tree_sitter.Language] = {
    _PYTHON: tree_sitter.Language(_TREESITTER_BUILD, _PYTHON),
    _C_SHARP: tree_sitter.Language(_TREESITTER_BUILD, _C_SHARP),
    _JAVA: tree_sitter.Language(_TREESITTER_BUILD, _JAVA),
}

_PYTHON_PARSER = tree_sitter.Parser()
_PYTHON_PARSER.set_language(LANGUAGES[_PYTHON])

_C_S_PARSER = tree_sitter.Parser()
_C_S_PARSER.set_language(LANGUAGES[_C_SHARP])

_JAVA_PARSER = tree_sitter.Parser()
_JAVA_PARSER.set_language(LANGUAGES[_JAVA])

_PARSERS: Dict[str, tree_sitter.Parser] = {
    _PYTHON: _PYTHON_PARSER,
    _C_SHARP: _C_S_PARSER,
    _JAVA: _JAVA_PARSER,
}

_ASTS: Dict[Path, tree_sitter.Tree] = {
        # Intentionally empty
}

def get_ast(for_file: FileInfo) -> tree_sitter.Tree:
    """
    get_ast checks if an AST for the path already has been computed, and returns that
    AST if it is the case. Otherwise, it will parse the file to a tree_sitter AST
    and return that tree.
    """
    try:
        ast = _ASTS[for_file.file_path]
    except KeyError:
        _ASTS[for_file.file_path] = _parse_ast(for_file)
        ast = _ASTS[for_file.file_path]
    finally:
        return ast


def _parse_ast(of_file: FileInfo) -> tree_sitter.Tree:
    """
    parses and returns the tree_sitter AST for a given file
    """
    with of_file.file_path.open("rb") as file:
        ast = _PARSERS[of_file.language].parse(file.read())
        if ast is None:
            raise TypeError(f"Abstract syntax tree for ${of_file} is None")
        return ast
