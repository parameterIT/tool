import logging
import json
import subprocess
from pathlib import Path
from typing import Dict, List
from tree_sitter import Parser, Language
import tree_sitter
from modu.source_repository.file_info import FileInfo
from modu.source_repository.languages import languages
import chardet

_TREESITTER_BUILD: Path = Path("build/my-languages.so")
_IGNORE_FILE_PATH: Path = Path("modu/util/.moduignore")
SUPPORTED_ENCODINGS: List[str] = [
    "ASCII",
    "ISO-8859-1",
    "UTF-8",
    # UTF-8-SIG files have a BOM, using UTF-8-SIG will correctly read the BOM as meta-data
    "UTF-8-SIG",
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
        # Get all files
        files = [f for f in self.src_root.glob("**/*") if f.is_file()]
        # Remove unwanted
        ignored_regex_list = self._get_ignore_regex_list()
        for ignore in ignored_regex_list:
            files = [file for file in files if not file.match(ignore)]
        # Check encoding
        if self.src_root.is_file():
            for ignore in ignored_regex_list:
                if self.src_root.match(ignore):
                    return {}
            return {self.src_root: self._inspect_file(self.src_root)}

        file_infos: Dict[Path, FileInfo] = self._discover_in_dir(files)

        return file_infos

    def _discover_in_dir(self, files: list) -> Dict[Path, FileInfo]:
        file_infos: Dict[Path, FileInfo] = {}
        for f in files:
            file_info = self._inspect_file(f)
            if not self._should_exclude(file_info):
                file_infos[f] = file_info
            else:
                file_info = self._inspect_file(f)
                if not self._should_exclude(file_info):
                    file_infos[f] = file_info
                else:
                    logging.warning(
                        f"Excluding {file_info.file_path} from analysis. (Language: {file_info.language}, encoding: {file_info.encoding})"
                    )

        return file_infos

    def _inspect_file(self, file_path: Path) -> FileInfo:
        if not file_path.is_file():
            raise ValueError(f"_inspect_file expects that ${file_path} is a file")

        programming_language: str = self._detect_language(file_path)

        encoding: str = UNKNOWN_ENCODING
        with file_path.open("rb") as file:
            chardet_guess = chardet.detect(file.read())
            if not chardet_guess["encoding"] is None:
                # encoding will be 'unknown' if chardet guesses it as None
                encoding = chardet_guess["encoding"].upper()

        return FileInfo(file_path, encoding, programming_language)

    def _detect_language(self, file_path: Path) -> str:
        res = subprocess.run(
            f"docker run --user $(id -u) -v $(pwd):$(pwd) -w $(pwd) -t linguist github-linguist --json {file_path}",
            shell=True,
            capture_output=True,
            text=True,
        )

        language = UNKNOWN_LANGUAGE
        try:
            res_dict = json.loads(res.stdout)
            # Use a formatted string to ensure that file_path is given as a key in the exact same way as it is given to
            # the linguist in the subprocess call, because it uses the file_path as it appears in the command as
            # the JSON (dictionary) key.
            language = res_dict[f"{file_path}"]["language"]
            if language is None:
                raise ValueError("linguist returns None language for empty file")
        except (json.decoder.JSONDecodeError, ValueError):
            language = self._read_suffix(file_path)
        finally:
            if language.lower() == "c#":
                language = "c_sharp"
            return language.lower()

    def _read_suffix(self, file_path: Path):
        match file_path.suffix:
            case ".py":
                return PYTHON
            case ".cs":
                return C_SHARP
            case ".java":
                return JAVA
            case _:
                return UNKNOWN_LANGUAGE

    def _get_ignore_regex_list(self):
        with _IGNORE_FILE_PATH.open("r") as file:
            ignored_files = []
            for line in file:
                ignored_files.append(line.rstrip())
        return ignored_files

    def _should_exclude(self, file_info: FileInfo):
        return (
            file_info.language == UNKNOWN_LANGUAGE
            or file_info.encoding == UNKNOWN_ENCODING
            or file_info.encoding not in SUPPORTED_ENCODINGS
        )
