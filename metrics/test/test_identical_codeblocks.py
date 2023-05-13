from pathlib import Path
import unittest
import os
from core.source_repository.source_repository import SourceRepository
from metrics.identical_codeblocks import IdenticalBlocksofCode


class TestIdenticalCodeBlocks(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_identical_codeblocks")
        )
        self._identicalcode = IdenticalBlocksofCode()
        self._identicalcode._source_repository = self._source_repository

    @unittest.skipIf(
        not os.path.exists("../../metrics/cpd"),
        "CPD doesn't exist in the environment",
    )
    def test_identical_codeblocks_given_file_returns_1(self):
        result = self._identicalcode.run()
        self.assertEqual(result.outcome, 1)
        # CPD reports the full path's, so will always be machine specific. Therefore, we test only that the reported
        # lines are correct and assume that these lines can only stem correctly from the expected files.
        duplications = result.get_violation_locations()
        lines_of_duplications = []
        for duplication in duplications:
            lines_of_duplication = []
            for location in duplication:
                lines_of_duplication.append((location[1], location[2]))
            lines_of_duplications.append(lines_of_duplication)

        expected_lines_of_duplications = [[(19, 28), (31, 40)]]
        self.assertCountEqual(lines_of_duplications, expected_lines_of_duplications)

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
