from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.similar_codeblocks import SimilarBlocksofCode


class TestSimilarCodeBlocks(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_similar_codeblocks"), "python"
        )
        self._similarcode = SimilarBlocksofCode()
        self._similarcode._source_repository = self._source_repository

    @unittest.skipIf(
        not os.path.exists("../../metrics/cpd"),
        "CPD doesn't exist in the environment",
    )
    def test_similar_codeblocks_given_file_returns_1(self):
        result = len(self._similarcode.run())
        self.assertEqual(result, 1)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
