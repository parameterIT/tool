from io import StringIO
import subprocess
from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository
from defusedxml.ElementTree import parse

TOKENS = 35


class SimilarBlocksofCode(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        return self.similar_blocks_of_code(
            [str(file) for file in self._source_repository.src_paths]
        )

    def similar_blocks_of_code(self, files) -> list:
        """
        Finds the amount of similar code blocks in a given repository
        """
        data = []
        filestring = f"{files}"
        filestring = filestring[1 : len(filestring) - 1]
        res = subprocess.run(
            f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --ignore-identifiers --ignore-literals --dir {filestring} --format xml",
            shell=True,
            capture_output=True,
            text=True,
        )
        et = parse(StringIO(res.stdout))
        for child in et.getroot():
            if child.tag == "duplication":
                duplicates = [
                    [
                        child.attrib["path"],
                        child.attrib["line"],
                        child.attrib["endline"],
                    ]
                    for child in child
                    if child.tag == "file"
                ]
                data.append(["Similar Code", duplicates])
        return data


metric = SimilarBlocksofCode()
