import subprocess
import unittest
import os

class TestMethodLength(unittest.TestCase):
    def test_method_length_given_too_long_file_returns_1(self):
        os.chdir("../../")
        cmd = ["./metrics/argument_count.py", "./metrics/test/data/test_data_method_length"]
        process = subprocess.run(cmd, capture_output=True)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "1")


if __name__ == "__main__":
    unittest.main()