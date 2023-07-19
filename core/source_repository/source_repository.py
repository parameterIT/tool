import json
import subprocess
from pathlib import Path
from typing import Dict
import tree_sitter
from core.source_repository.file_info import FileInfo
import chardet

_IGNORE_FILE_PATH: Path = Path("core/util/.moduignore")

UNKNOWN_ENCODING = "unknown"
UNKNOWN_LANGUAGE = "unknown"

PYTHON = "python"
C_SHARP = "c_sharp"
JAVA = "java"

class SourceRepository:
    """
    contains all information accessible by metrics about the source code
    under analysis
    """

    def __init__(self, src_root: Path):
        self.src_root: Path = src_root
        self.asts: Dict[Path, tree_sitter.Tree] = {}
        self.ignored_glob_regex_list = self._get_ignore_regex_list()
        self.files: Dict[Path, FileInfo] = self._discover_files()

    def _discover_files(self) -> Dict[Path, FileInfo]:
        if self.src_root.is_file():
            for ignore in self.ignored_glob_regex_list:
                if self.src_root.match(ignore):
                    return {}
            return {self.src_root: self._inspect_file(self.src_root)}

        files = self._get_filtered_files(self.src_root)

        file_infos: Dict[Path, FileInfo] = self._inspect_files(files)

        return file_infos

    def _inspect_files(self, files: list) -> Dict[Path, FileInfo]:
        file_infos: Dict[Path, FileInfo] = {}
        for f in files:
            file_info = self._inspect_file(f)
            file_infos[f] = file_info
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

    def _get_filtered_files(self, root_dir: Path):
        files = []
        for f in root_dir.iterdir():
            ignored = False
            for ignore in self.ignored_glob_regex_list:
                if f.match(ignore):
                    ignored = True
            if not ignored:
                if f.is_dir():
                    files.extend(self._get_filtered_files(f))
                else:
                    files.append(f)
        return files

    def _get_ignore_regex_list(self):
        if not _IGNORE_FILE_PATH.exists():
            return []

        with _IGNORE_FILE_PATH.open("r") as file:
            ignored_files = []
            for line in file:
                ignored_files.append(line.rstrip())
        return ignored_files
