from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
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
        result = Result("identical code", [])
        for encoding in set(self._source_repository.file_encodings.values()):
            files = [
                str(file)
                for file, encoding_type in self._source_repository.file_encodings.items()
                if encoding_type == encoding
            ]
            print(encoding)
            if encoding == "UTF-8-SIG":
                encoding = "UTF-8"
            if encoding == "ascii":
                encoding = "US-ASCII"
            print(len(files))
            filestring = f"{files}"
            filestring = filestring[1 : len(filestring) - 1]
            res = subprocess.run(
                f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --dir {filestring} --format xml --encoding {encoding}",
                shell=True,
                capture_output=True,
                text=True,
            )
            print(res.stdout == "")
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
                    result.violations.append(Violation("identical code", duplicates))
        return result


metric = IdenticalBlocksofCode()
