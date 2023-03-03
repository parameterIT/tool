import subprocess
import unittest
import os

class TestArgumentCount(unittest.TestCase):
    def test_argument_count_given_directory_returns_2(self):
        os.chdir("../../")
        cmd = ["./metrics/argument_count.py", "./metrics/test/data/test_data_argument_count"]
        process = subprocess.run(cmd, capture_output=True)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "2")


if __name__ == "__main__":
    unittest.main()