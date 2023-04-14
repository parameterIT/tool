import logging
from pathlib import Path
from typing import Dict, List
from tree_sitter import Parser, Language
import tree_sitter
from byoqm.source_repository.file_info import FileInfo
from byoqm.source_repository.languages import languages
import chardet

_TREESITTER_BUILD: Path = Path("build/my-languages.so")


class SourceRepository:
    """
    contains all information accessible by metrics about the source code
    under analysis
    """

    def __init__(self, src_root: Path):
        self.src_root: Path = src_root
        self.asts: Dict[Path, tree_sitter.Tree] = {}
        self.files: List[FileInfo] = []

    def getAst(self, for_file: Path) -> tree_sitter.Tree:
        """
        getAst checks if an AST for the path already has been computed, and returns that
        AST if it is the case. Otherwise, it will parse the file to a tree_sitter AST
        and return that tree.

        Throws a ValueError when the file to parse is not a child path of the given
        src_root.
        """
        if for_file not in self.src_paths:
            logging.error("The file to parse must be a child path of of the src_root")
            raise ValueError

        ast = None
        try:
            ast = self.asts[for_file]
        except KeyError:
            self.asts[for_file] = self._parse_ast(for_file)
            ast = self.asts[for_file]
        finally:
            return ast

    def _parse_ast(self, file_at: Path) -> tree_sitter.Tree:
        """
        parses and returns the tree_sitter AST for a given file
        """
        try:
            with file_at.open("rb") as file:
                ast = self._parser.parse(file.read())
                return ast
        except Exception as e:
            logging.error(
                f"Failed to parse ast for file at path: {file_at} with encoding {self.file_encodings[file_at]}. Error: {e}"
            )
            raise e

    def _get_encodings(self, files):
        encodings = {}
        temp = []
        for file in files:
            with file.open("rb") as f:
                encoding = chardet.detect(f.read())["encoding"]
                match encoding:
                    case "UTF-8-SIG":
                        encoding = "UTF-8"
                    case "utf-8":
                        encoding = "UTF-8"
                    case "UTF-16BE":
                        encoding = "UTF-16BE"
                    case "UTF-16LE":
                        encoding = "UTF-16LE"
                    case "UTF-16":
                        encoding = "UTF-16"
                    case "ascii":
                        encoding = "US-ASCII"
                    case "ISO-8859-1":
                        encoding = "ISO-8859-1"
                    case _:
                        temp.append(file)
                        continue
                encodings[file] = encoding

        self.src_paths = [file for file in self.src_paths if file not in temp]
        return encodings
