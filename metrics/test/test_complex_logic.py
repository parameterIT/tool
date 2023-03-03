from pathlib import Path
import subprocess
import unittest
import os

class TestComplexLogic(unittest.TestCase):
    def setUp(self):
        os.chdir("../../")

    def test_complex_logic_given_file_returns_4(self):
        cmd = ["./metrics/complex_logic.py", "./metrics/test/data/test_data_complex_logic"]
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        self.assertEqual(result, "4")
    
    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())
        
if __name__ == "__main__":
    unittest.main()