from pathlib import Path
import subprocess
import unittest
import os


class TestArgumentCount(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")

    def test_argument_count_given_directory_returns_1(self):
        cmd = [
            "./metrics/argument_count.py",
            "./metrics/test/data/test_data_argument_count",
        ]
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "2")

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
