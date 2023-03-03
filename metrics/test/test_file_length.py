from pathlib import Path
import subprocess
import unittest
import os

class TestFileLength(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")

    def test_file_length_given_file_returns_1(self):
        cmd = ["./metrics/file_length.py", "./metrics/test/data/test_data_file_length"]
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "1")
    
    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())
        
if __name__ == "__main__":
    unittest.main()