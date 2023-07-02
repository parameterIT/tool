from pathlib import Path
import unittest
import os
from core.source_repository.source_repository import SourceRepository
from metrics.similar_codeblocks import SimilarBlocksofCode


class TestSimilarCodeBlocks(unittest.TestCase):
    def setUp(self):
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_similar_codeblocks")
        )
        self._similarcode = SimilarBlocksofCode()
        self._similarcode._source_repository = self._source_repository

    @unittest.skipIf(
        not os.path.exists("metrics/cpd"),
        "CPD doesn't exist in the environment",
    )
    def test_similar_codeblocks_given_file_returns_1(self):
        result = self._similarcode.run()
        self.assertEqual(result.outcome, 1)
        # CPD reports the full path's, so will always be machine specific. Therefore, we test only that the reported
        # lines are correct and assume that these lines can only stem correctly from the expected files.
        lines = [
            (loc.first_line, loc.last_line) for loc in result.get_violation_locations()
        ]

        expected_lines = [(3, 11), (16, 24)]
        self.assertCountEqual(lines, expected_lines)


if __name__ == "__main__":
    unittest.main()
