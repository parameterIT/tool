from io import StringIO
import subprocess
from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository
from defusedxml.ElementTree import parse

TOKENS = 35


class SimilarBlocksofCode(Metric):
    def __init__(self):
        self.coordinator: SourceRepository = None

    def run(self):
        return self.similar_blocks_of_code(
            [str(file) for file in self.coordinator.src_paths]
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
                data.append(["Similar Codeblocks", "find way to get file", 1, 1])
        return data


metric = SimilarBlocksofCode()
