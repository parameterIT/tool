from pathlib import Path
import unittest
import os
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from metrics.similar_codeblocks import SimilarBlocksofCode


class TestSimilarCodeBlocks(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")
        self._coordinator = SourceCoordinator(Path("./metrics/test/data/test_data_similar_codeblocks"),"python")
        self._similarcode = SimilarBlocksofCode()
        self._similarcode.set_coordinator(self._coordinator)
        
    @unittest.skipIf(
        not os.path.exists("../../metrics/cpd"),
        "CPD doesn't exist in the environment",
    )
    def test_similar_codeblocks_given_file_returns_1(self):
        result = self._similarcode.run()
        self.assertEqual(result, 1)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
