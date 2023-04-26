from io import StringIO
from typing import List
import subprocess
from modu.metric.metric import Metric
from modu.metric.result import Result
from modu.metric.violation import Violation
from modu.source_repository.source_repository import SourceRepository
from defusedxml.ElementTree import parse

TOKENS = 35

_CHARDET_ENCODINGS_TO_CPD = {
    "ASCII": "US-ASCII",
    "ISO-8859-1": "ISO-8859-1",
    "UTF-8": "UTF-8",
    "UTF-8-SIG": "UTF-8",
    "UTF-16": "UTF-16",
    "UTF-16BE": "UTF-16BE",
    "UTF-16LE": "UTF-16LE",
}


class SimilarBlocksofCode(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        return self._similar_blocks_of_code()

    def _similar_blocks_of_code(self) -> Result:
        """
        Finds the amount of similar code blocks in a given repository
        """
        violations = []
        to_inspect = [
            str(file)
            for file, file_info in self._source_repository.files.items()
            if file_info.encoding in _CHARDET_ENCODINGS_TO_CPD
        ]
        to_inspect = str(to_inspect)
        to_inspect = to_inspect[1 : (len(to_inspect) - 1)]
        res = subprocess.run(
            f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --ignore-identifiers --ignore-literals --dir {to_inspect} --format xml",
            shell=True,
            capture_output=True,
            text=True,
        )
        element_tree = parse(StringIO(res.stdout))
        for child in element_tree.getroot():
            if child.tag == "duplication":
                duplicates = [
                    (
                        child.attrib["path"],
                        int(child.attrib["line"]),
                        int(child.attrib["endline"]),
                    )
                    for child in child
                    if child.tag == "file"
                ]
                violations.append(Violation("similar code", duplicates))
        return Result("similar code", violations, len(violations))


metric = SimilarBlocksofCode()
