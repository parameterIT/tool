from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter


_TREESITTER_BUILD: Path = Path("build/my-languages.so").resolve()


class SourceCoordinator:
    def __init__(self, src_root: Path, langauge: str):
        self.src_root = src_root
        self.language = Language(_TREESITTER_BUILD.__str__(), langauge)
        self.asts = {}

        self._parser = Parser()
        self._parser.set_language(self.language)

    def getAst(self, for_file: Path):
        if not for_file.is_relative_to(self.src_root):
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
