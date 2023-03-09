from io import StringIO
import subprocess
from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from defusedxml.ElementTree import parse

TOKENS = 35


class SimilarBlocksofCode(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = self.similar_blocks_of_code(
            [str(file) for file in self.coordinator.src_paths]
        )
        return count

    def similar_blocks_of_code(self, files) -> int | float:
        filestring = f"{files}"
        filestring = filestring[1 : len(filestring) - 1]
        count = 0
        res = subprocess.run(
            f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --ignore-identifiers --ignore-literals --dir {filestring} --format xml",
            shell=True,
            capture_output=True,
            text=True,
        )
        et = parse(StringIO(res.stdout))
        for child in et.getroot():
            if child.tag == "duplication":
                count += 1
        return count


metric = SimilarBlocksofCode()
