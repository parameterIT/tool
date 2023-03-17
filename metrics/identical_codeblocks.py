from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository
from defusedxml.ElementTree import parse
from io import StringIO
import subprocess

TOKENS = 35


class IdenticalBlocksofCode(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        return self.identical_blocks_of_code(
            [str(file) for file in self._source_repository.src_paths]
        )

    def identical_blocks_of_code(self, files) -> list:
        """
        Finds the amount of identical code blocks that exist in the given code base.

        Makes use of Copy Paste Detector (CPD)
        """
        data = []
        filestring = f"{files}"
        filestring = filestring[1 : len(filestring) - 1]
        res = subprocess.run(
            f"metrics/cpd/bin/run.sh cpd --minimum-tokens {TOKENS} --skip-lexical-errors --dir {filestring} --format xml",
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
                    for child in child if child.tag == 'file'
                ]
                data.append(["Identical Code", duplicates])
        return data


metric = IdenticalBlocksofCode()
