from pathlib import Path
import subprocess
import unittest
import os


class TestIdenticalCodeBlocks(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")

    @unittest.skipIf(
        not os.path.exists("../../metrics/cpd"),
        "CPD doesn't exist in the environment",
    )
    def test_identical_codeblocks_given_file_returns_1(self):
        cmd = [
            "./metrics/identical_codeblocks.py",
            "./metrics/test/data/test_data_identical_codeblocks",
        ]
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "1")

    @unittest.skipIf(
        not os.path.exists("../../metrics/cpd"),
        "CPD doesn't exist in the environment",
    )
    def test_identical_codeblocks_given_file_returns_2(self):
        cmd = [
            "./metrics/identical_codeblocks.py",
            "./metrics/test/data/test_data_identical_codeblocks",
        ]
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "1")

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
