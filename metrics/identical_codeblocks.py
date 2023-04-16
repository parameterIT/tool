from modu.metric.metric import Metric
from modu.metric.result import Result
from modu.metric.violation import Violation
from modu.source_repository.source_repository import SourceRepository
from defusedxml.ElementTree import parse
from io import StringIO
import subprocess

TOKENS = 35

_CHARDET_ENCODINGS_TO_CPD = {
    "ASCII": "US-ASCII",
    "ISO-8859-1": "ISO-8859-1",
    "UTF-8": "UTF-8",
    "UTF-16": "UTF-16",
    "UTF-16BE": "UTF-16BE",
    "UTF-16LE": "UTF-16LE",
}


class IdenticalBlocksofCode(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self) -> Result:
        return self._identical_blocks_of_code()

    def _identical_blocks_of_code(self) -> Result:
        """
        Finds the amount of identical code blocks that exist in the given code base.

        Makes use of Copy Paste Detector (CPD)
        """
        violations = []
        for file, file_info in self._source_repository.files.items():
            filestring = f"{file}"
            cpd_encoding = _CHARDET_ENCODINGS_TO_CPD[file_info.encoding]

            res = subprocess.run(
                f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --dir {filestring} --format xml --encoding {cpd_encoding}",
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
                    violations.append(Violation("identical code", duplicates))
        return Result("identical code", violations, len(violations))


metric = IdenticalBlocksofCode()
