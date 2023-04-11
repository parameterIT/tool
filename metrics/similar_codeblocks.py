from io import StringIO
from typing import List
import subprocess
from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from defusedxml.ElementTree import parse

TOKENS = 35


class SimilarBlocksofCode(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        return self._similar_blocks_of_code(
            [str(file) for file in self._source_repository.src_paths]
        )

    def _similar_blocks_of_code(self, files) -> Result:
        """
        Finds the amount of similar code blocks in a given repository
        """
        result = Result("similar code", [])
        for encoding in set(self._source_repository.file_encodings.values()):
            files = [
                str(file)
                for file, encoding_type in self._source_repository.file_encodings.items()
                if encoding_type == encoding
            ]
            filestring = f"{files}"
            filestring = filestring[1 : len(filestring) - 1]
            res = subprocess.run(
                f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --dir {filestring} --format xml --encoding {encoding}",
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
                    result.violations.append(Violation("similar code", duplicates))
        return result


metric = SimilarBlocksofCode()
