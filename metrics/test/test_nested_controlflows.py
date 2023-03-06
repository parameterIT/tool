from pathlib import Path
import subprocess
import unittest
import os


class TestNestedControlFlows(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")
    @unittest.expectedFailure
    def test_nested_controlflow_given_test_directory_returns_9(self):
        cmd = [
            "./metrics/nested_controlflows.py",
            "./metrics/test/data/test_data_nested_controlflows",
        ]
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "9")

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
