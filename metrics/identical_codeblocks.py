from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation, Location
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import SUPPORTED_ENCODINGS
from defusedxml.ElementTree import parse
from io import StringIO
import subprocess

TOKENS = 35


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
        to_inspect = [
            str(file)
            for file, file_info in self._source_repository.files.items()
            if file_info.encoding in SUPPORTED_ENCODINGS
        ]
        to_inspect = str(to_inspect)
        to_inspect = to_inspect[1 : (len(to_inspect) - 1)]
        res = subprocess.run(
            f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --dir {to_inspect} --format xml",
            shell=True,
            capture_output=True,
            text=True,
        )
        element_tree = parse(StringIO(res.stdout))
        for child in element_tree.getroot():
            if child.tag == "duplication":
                duplicates = [
                    Location(
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
