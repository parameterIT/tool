import logging
import os
from pathlib import Path
from typing import Dict, List
from tree_sitter import Parser, Language
import tree_sitter
from byoqm.source_repository.file_info import FileInfo
from byoqm.source_repository.languages import languages
import chardet

_TREESITTER_BUILD: Path = Path("build/my-languages.so")
_IGNORE_FILE_PATH: Path = Path("byoqm/util/.ignore_paths.txt")
_IGNORE_FILE_EXTENSIONS_PATH: Path = Path("byoqm/util/.ignore_extensions.txt")
SUPPORTED_ENCODINGS: List[str] = [
    "ASCII",
    "ISO-8859-1",
    "UTF-8",
    "UTF-16BE",
    "UTF-16LE",
    "UTF-16",
]
UNKNOWN_ENCODING = "unknown"

PYTHON = "python"
C_SHARP = "c_sharp"
JAVA = "java"
UNKNOWN_LANGUAGE = "unknown"


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
            PYTHON: tree_sitter.Language(_TREESITTER_BUILD, PYTHON),
            C_SHARP: tree_sitter.Language(_TREESITTER_BUILD, C_SHARP),
            JAVA: tree_sitter.Language(_TREESITTER_BUILD, JAVA),
        }

        python_parser = tree_sitter.Parser()
        python_parser.set_language(self.tree_sitter_languages[PYTHON])

        c_sharp_parser = tree_sitter.Parser()
        c_sharp_parser.set_language(self.tree_sitter_languages[C_SHARP])

        java_parser = tree_sitter.Parser()
        java_parser.set_language(self.tree_sitter_languages[JAVA])

        self.tree_sitter_parsers: Dict[str, tree_sitter.Parser] = {
            PYTHON: python_parser,
            C_SHARP: c_sharp_parser,
            JAVA: java_parser,
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
        ignored_files = self._get_ignored_files()

        if self.src_root.is_file():
            if self.src_root in ignored_files:
                logging.warning(
                    "Source directory is a file and is included in the .ignore file"
                )
                return {}
            return {self.src_root: self._inspect_file(self.src_root)}

        file_infos: Dict[Path, FileInfo] = self._discover_in_dir(
            self.src_root, ignored_files
        )

        return file_infos

    def _discover_in_dir(self, root_dir: Path, ignored_files) -> Dict[Path, FileInfo]:
        file_infos: Dict[Path, FileInfo] = {}
        for f in root_dir.iterdir():
            if f in ignored_files:
                continue
            if f.is_dir():
                file_infos.update(self._discover_in_dir(f, ignored_files))
            else:
                file_info = self._inspect_file(f)
                if not self._should_exclude(file_info):
                    file_infos[f] = file_info
                else:
                    logging.warn(
                        f"Excluding f{file_info.file_path} from analysis. (Language: {file_info.language}, encoding: {file_info.encoding})"
                    )

        return file_infos

    def _inspect_file(self, file_path: Path) -> FileInfo:
        if not file_path.is_file():
            raise ValueError(f"_inspect_file expects that ${file_path} is a file")

        programming_language: str = UNKNOWN_LANGUAGE
        match file_path.suffix:
            case ".py":
                programming_language = PYTHON
            case ".cs":
                programming_language = C_SHARP
            case ".java":
                programming_language = JAVA
            case _:
                programming_language = UNKNOWN_LANGUAGE

        encoding: str = UNKNOWN_ENCODING
        with file_path.open("rb") as file:
            chardet_guess = chardet.detect(file.read())
            if not chardet_guess["encoding"] is None:
                # encoding will be 'unknown' if chardet guesses it as None
                encoding = chardet_guess["encoding"].upper()

        return FileInfo(file_path, encoding, programming_language)

    def _get_ignored_files(self):
        ignored_files = self._get_ignored_paths()
        ignored_files.extend(self.get_ignored_file_extensions())
        return ignored_files

    def _get_ignored_paths(self):
        with _IGNORE_FILE_PATH.open("r") as file:
            ignored_files = []
            for line in file:
                path = Path(line.rstrip())
                if path.is_dir():
                    ignored_files.extend(path.glob("*"))
                if path.is_file():
                    ignored_files.append(path)
        return ignored_files

    def get_ignored_file_extensions(self):
        with _IGNORE_FILE_EXTENSIONS_PATH.open("r") as file:
            ignored_files = []
            for extension in file:
                ignored_files.extend(self.src_root.glob(f"**/*{extension.rstrip()}"))
        return ignored_files

    def _should_exclude(self, file_info: FileInfo):
        return (
            file_info.language == UNKNOWN_LANGUAGE
            or file_info.encoding == UNKNOWN_ENCODING
            or file_info.encoding not in SUPPORTED_ENCODINGS
        )
