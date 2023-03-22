from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.identical_codeblocks import IdenticalBlocksofCode


class TestIdenticalCodeBlocks(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_identical_codeblocks"), "python"
        )
        self._identicalcode = IdenticalBlocksofCode()
        self._identicalcode._source_repository = self._source_repository

    @unittest.skipIf(
        not os.path.exists("../../metrics/cpd"),
        "CPD doesn't exist in the environment",
    )
    def test_identical_codeblocks_given_file_returns_1(self):
        result = self._identicalcode.run()
        self.assertEqual(result.get_frequency(), 1)
        locations = result.get_violation_locations()[0]
        first_code_block = (locations[0][1], locations[0][2])
        second_code_block = (locations[1][1], locations[1][2])
        self.assertEqual(first_code_block, (19, 28))
        self.assertEqual(second_code_block, (31, 40))

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
