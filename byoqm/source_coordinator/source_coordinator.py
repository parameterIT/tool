from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter


_TREESITTER_BUILD: Path = Path("build/my-languages.so")


class SourceCoordinator:
    def __init__(self, src_root: Path, langauge: str):
        if src_root.is_file():
            self.src_paths = [src_root]
        else:
            self.src_paths = [file for file in src_root.glob("**/*.py")]

        self.language = Language(_TREESITTER_BUILD.__str__(), langauge)
        self.asts = {}

        self._parser = Parser()
        self._parser.set_language(self.language)

    def getAst(self, for_file: Path) -> tree_sitter.Tree:
        """
        getAst checks if an AST for the path already has been computed, and returns that
        AST if it is the case. Otherwise, it will parse the file to a tree_sitter AST
        and return that tree.

        Throws a ValueError when the file to parse is not a child path of the given
        src_root.
        """
        if for_file not in self.src_paths:
            raise ValueError(
                "The file to parse must be a child path of of the src_root"
            )

        ast = None
        try:
            ast = self.asts[for_file]
        except KeyError:
            self.asts[for_file] = self._parse_ast(for_file)
            ast = self.asts[for_file]
        finally:
            return ast

    def _parse_ast(self, file_at: Path) -> tree_sitter.Tree:
        with file_at.open() as file:
            ast = self._parser.parse(bytes(file.read(), "utf8"))
            return ast
