import logging
from pathlib import Path
from typing import Dict, List
from tree_sitter import Parser, Language
import tree_sitter
from byoqm.source_repository.file_info import FileInfo
from byoqm.source_repository.languages import languages
import chardet

_TREESITTER_BUILD: Path = Path("build/my-languages.so")
_SUPPORTED_ENCODINGS: List[str] = [
    "ascii",
    "ISO-8859-1",
    "utf-8",
    "UTF-16BE",
    "UTF-16LE",
    "UTF-16",
]


class SourceRepository:
    """
    contains all information accessible by metrics about the source code
    under analysis
    """

    def __init__(self, src_root: Path):
        self.src_root: Path = src_root
        self.asts: Dict[Path, tree_sitter.Tree] = {}
        self.files: Dict[Path, FileInfo] = self._discover_files()
        self.tree_sitter_languages: Dict[str, tree_sitter.Language] = {
            "python": tree_sitter.Language(_TREESITTER_BUILD, "python"),
            "c_sharp": tree_sitter.Language(_TREESITTER_BUILD, "c_sharp"),
            "java": tree_sitter.Language(_TREESITTER_BUILD, "java"),
        }

        python_parser = tree_sitter.Parser()
        python_parser.set_language(self.tree_sitter_languages["python"])

        c_sharp_parser = tree_sitter.Parser()
        c_sharp_parser.set_language(self.tree_sitter_languages["c_sharp"])

        java_parser = tree_sitter.Parser()
        java_parser.set_language(self.tree_sitter_languages["java"])

        self.tree_sitter_parsers: Dict[str, tree_sitter.Parser] = {
            "python": python_parser,
            "c_sharp": c_sharp_parser,
            "java": java_parser,
        }

    def get_ast(self, for_file: FileInfo) -> tree_sitter.Tree:
        """
        get_ast checks if an AST for the path already has been computed, and returns that
        AST if it is the case. Otherwise, it will parse the file to a tree_sitter AST
        and return that tree.
        """
        ast = None
        try:
            ast = self.asts[for_file.file_path]
            return ast
        except KeyError:
            self.asts[for_file.file_path] = self._parse_ast(for_file)
            ast = self.asts[for_file.file_path]
            return ast

    def _parse_ast(self, of_file: FileInfo) -> tree_sitter.Tree:
        """
        parses and returns the tree_sitter AST for a given file
        """
        with of_file.file_path.open("rb") as file:
            ast = self.tree_sitter_parsers[of_file.language].parse(file.read())
            if ast is None:
                raise TypeError(f"Abstract syntax tree for ${of_file} is None")
            return ast

    def _discover_files(self) -> Dict[Path, FileInfo]:
        if self.src_root.is_file():
            return {self.src_root: self._inspect_file(self.src_root)}

        file_infos: Dict[Path, FileInfo] = self._discover_in_dir(self.src_root)
        return file_infos

    def _discover_in_dir(self, root_dir: Path) -> Dict[Path, FileInfo]:
        file_infos: Dict[Path, FileInfo] = {}
        for f in root_dir.iterdir():
            if f.is_dir():
                file_infos.update(self._discover_in_dir(f))
            else:
                file_info = self._inspect_file(f)
                if not self._should_exclude(file_info):
                    file_infos[f] = file_info

        return file_infos

    def _inspect_file(self, file_path: Path) -> FileInfo:
        if not file_path.is_file():
            raise ValueError(f"_inspect_file expects that ${file_path} is a file")

        programming_language: str = "unknown"
        if file_path.suffix == ".py":
            programming_language = "python"
        elif file_path.suffix == ".cs":
            programming_language = "c_sharp"
        elif file_path.suffix == ".java":
            programming_language = "java"

        encoding: str = "unknown"
        if file_path.suffix != ".jar":
            with file_path.open("rb") as file:
                chardet_guess = chardet.detect(file.read())
                if not chardet_guess["encoding"] is None:
                    # encoding will be 'unknown' if chardet guesses it as None
                    encoding = chardet_guess["encoding"]

        return FileInfo(file_path, encoding, programming_language)

    def _should_exclude(self, file_info: FileInfo):
        return (
            file_info.language == "unknown"
            or file_info.encoding == "unknown"
            or file_info.encoding not in _SUPPORTED_ENCODINGS
        )

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
