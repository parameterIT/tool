from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from defusedxml.ElementTree import parse
from io import StringIO
import subprocess

TOKENS = 35


class IdenticalBlocksofCode(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = self.identical_blocks_of_code(
            [str(file) for file in self.coordinator.src_paths]
        )
        return count

    def identical_blocks_of_code(self, files) -> int | float:
        """
        Finds the amount of identical code blocks that exist in the given code base. 
        
        Makes use of Copy Paste Detector (CPD)
        """
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


metric = IdenticalBlocksofCode()
