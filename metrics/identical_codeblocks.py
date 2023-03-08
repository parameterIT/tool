#!/usr/bin/env python
from pathlib import Path
from tree_sitter import Language, Parser
import sys
from defusedxml.ElementTree import parse
from io import StringIO
import subprocess


def parse_src_root() -> Path:
    if len(sys.argv) == 1:
        print("Make sure to provide the path to source code")
        exit(1)

    path_to_src = Path(sys.argv[1])
    if not path_to_src.exists():
        print(f"The source code at {path_to_src.resolve()} does not exist")
        exit(1)

    return path_to_src


TOKENS = 35
PY_LANGUAGE = Language("./build/my-languages.so", "python")
parser = Parser()
parser.set_language(PY_LANGUAGE)
src_root = parse_src_root()


def identical_blocks_of_code() -> int | float:
    files = []
    if src_root.is_file():
        files = [str(src_root)]
    else:
        files = [str(file) for file in src_root.glob("**/*.py")]
    filestring = f"{files}"
    filestring = filestring[1 : len(filestring) - 1]
    count = 0
    res = subprocess.run(
        f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --dir {filestring} --format xml",
        shell=True,
        capture_output=True,
        text=True,
    )
    et = parse(StringIO(res.stdout))
    for child in et.getroot():
        if child.tag == "duplication":
            count += 1
    return count


print(identical_blocks_of_code())
