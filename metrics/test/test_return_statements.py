from pathlib import Path
import subprocess
import unittest
import os

class TestReturnStatements(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")

    def test_return_statements_given_file_returns_2(self):
        cmd = ["./metrics/return_statements.py", "./metrics/test/data/test_data_return_statements"]
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "2")
    
    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())
        
if __name__ == "__main__":
    unittest.main()